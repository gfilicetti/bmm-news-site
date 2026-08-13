import os, urllib.request, json, subprocess, re
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")

# Use numeric GCP Project Number 159619652659 for Discovery Engine IAM compliance
PROJECT_NUMBER = "159619652659"
DATASTORE_ID = "bmm-site-1_1785864019095"
BASE_DS_URL = f"https://discoveryengine.googleapis.com/v1/projects/{PROJECT_NUMBER}/locations/global/collections/default_collection/dataStores/{DATASTORE_ID}"
SEARCH_API_URL = f"{BASE_DS_URL}/servingConfigs/default_search:search"
ANSWER_API_URL = f"{BASE_DS_URL}/servingConfigs/default_search:answer"
SESSIONS_API_URL = f"{BASE_DS_URL}/sessions"

def get_access_token():
    # 1. Try Cloud Run Metadata Server
    try:
        req = urllib.request.Request(
            "http://metadata.google.internal/computeMetadata/v1/instance/service-account/default/token",
            headers={"Metadata-Flavor": "Google"}
        )
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if "access_token" in data:
                return data["access_token"]
    except Exception as e:
        print("Metadata server token check failed:", e)

    # 2. Try google-auth library
    try:
        import google.auth
        import google.auth.transport.requests
        credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        if credentials.token:
            return credentials.token
    except Exception as e:
        print("google.auth token refresh failed:", e)

    # 3. Local dev fallback (gcloud CLI)
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"], timeout=5).decode().strip()
        if token:
            return token
    except Exception as e:
        print("gcloud token check failed:", e)

    return None

def create_discovery_session(token):
    try:
        req = urllib.request.Request(
            SESSIONS_API_URL,
            data=json.dumps({"userPseudoId": "bmm-guest"}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            sess_data = json.loads(resp.read().decode("utf-8"))
            return sess_data.get("name")
    except Exception as e:
        print("Error creating Discovery Engine session:", e)
        return None

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory(".", path)
    return send_from_directory(".", "index.html"), 404

def ensure_inline_footnotes(answer_text, references):
    if not answer_text or not references:
        return answer_text

    # If answer_text already contains inline footnotes like [1], [2], keep as is
    if re.search(r'\[\d+\]', answer_text):
        return answer_text

    # Inject footnote badges [1], [2], etc. matching references
    ref_count = len(references)
    if ref_count == 1:
        text_str = answer_text.strip()
        if not text_str.endswith(" [1]"):
            return text_str + " [1]"
        return text_str
    else:
        sentences = re.split(r'(?<=[.!?])\s+', answer_text.strip())
        for idx, ref in enumerate(references):
            num = idx + 1
            title = ref.get("title", "").lower()
            words = [w for w in re.findall(r'\w+', title) if len(w) > 3 and w not in ["news", "article", "breakthrough", "bmm"]]
            
            matched = False
            for s_idx, s in enumerate(sentences):
                s_lower = s.lower()
                if any(w in s_lower for w in words):
                    if f"[{num}]" not in sentences[s_idx]:
                        sentences[s_idx] += f" [{num}]"
                    matched = True
                    break
            
            if not matched:
                s_target = min(idx, len(sentences) - 1)
                if f"[{num}]" not in sentences[s_target]:
                    sentences[s_target] += f" [{num}]"

        return " ".join(sentences)

@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()
    session_id = data.get("sessionId")

    if not query:
        return jsonify({"results": [], "summary": None, "sessionId": None}), 200

    token = get_access_token()
    if not token:
        return jsonify({"error": "Failed to obtain GCP authentication token"}), 500

    if session_id:
        # Turn 2..N Follow-Up Query in Session using Discovery Engine Answer API
        payload = {
            "query": {"text": query},
            "session": session_id
        }
        req = urllib.request.Request(
            ANSWER_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                api_res = json.loads(resp.read().decode("utf-8"))
                answer_obj = api_res.get("answer", {})
                answer_text = answer_obj.get("answerText", "")

                references = []
                seen_uris = set()
                for step in answer_obj.get("steps", []):
                    for action in step.get("actions", []):
                        obs = action.get("observation", {})
                        for sr in obs.get("searchResults", []):
                            uri = sr.get("uri", "")
                            title = sr.get("title", "")
                            doc_name = sr.get("document", "")
                            if uri and uri not in seen_uris:
                                seen_uris.add(uri)
                                link_path = uri
                                if uri.startswith("http"):
                                    from urllib.parse import urlparse
                                    parsed = urlparse(uri)
                                    if parsed.path:
                                        link_path = parsed.path
                                references.append({
                                    "title": title or "Referenced Article",
                                    "document": doc_name,
                                    "uri": uri,
                                    "link": link_path
                                })

                formatted_answer_text = ensure_inline_footnotes(answer_text, references)

                return jsonify({
                    "sessionId": session_id,
                    "summary": {
                        "summaryText": formatted_answer_text,
                        "summaryWithMetadata": {
                            "references": references
                        }
                    },
                    "results": []
                }), 200
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            print(f"Discovery Engine Answer HTTP Error {e.code}: {err_body}")
            return jsonify({"error": f"Agent Search Error {e.code}", "details": err_body}), e.code
        except Exception as e:
            print("Discovery Engine Request Error:", e)
            return jsonify({"error": str(e)}), 500
    else:
        # Turn 1 Initial Query: Get AI Summary with summarySpec and create Session ID
        session_id = create_discovery_session(token)
        payload = {
            "query": query,
            "pageSize": 10,
            "contentSearchSpec": {
                "summarySpec": {
                    "summaryResultCount": 5,
                    "includeCitations": True
                },
                "snippetSpec": {
                    "maxSnippetCount": 1
                }
            }
        }
        req = urllib.request.Request(
            SEARCH_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                api_res = json.loads(resp.read().decode("utf-8"))
                api_res["sessionId"] = session_id
                return jsonify(api_res), 200
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            print(f"Discovery Engine HTTP Error {e.code}: {err_body}")
            return jsonify({"error": f"Agent Search Error {e.code}", "details": err_body}), e.code
        except Exception as e:
            print("Discovery Engine Request Error:", e)
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)

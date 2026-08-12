import os, urllib.request, json, subprocess
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")

# Use numeric GCP Project Number 159619652659 for Discovery Engine IAM compliance
PROJECT_NUMBER = "159619652659"
DATASTORE_ID = "bmm-site-1_1785864019095"
SEARCH_API_URL = f"https://discoveryengine.googleapis.com/v1/projects/{PROJECT_NUMBER}/locations/global/collections/default_collection/dataStores/{DATASTORE_ID}/servingConfigs/default_search:search"

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

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory(".", path)
    return send_from_directory(".", "index.html"), 404

@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"results": [], "summary": None}), 200

    token = get_access_token()
    if not token:
        return jsonify({"error": "Failed to obtain GCP authentication token"}), 500

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

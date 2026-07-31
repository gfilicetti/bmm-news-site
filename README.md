# BMM News Site

**BMM - The Most Trusted Brand in News**

A fast, responsive, containerized static news website showcasing breaking news, world headlines, and featured articles. The application is served using Nginx and optimized for deployment on **Google Cloud Run**.

---

## 📁 Repository Structure

- [`index.html`](index.html) — Main homepage featuring breaking news tickers, lead stories, story grids, and top headlines.
- [`styles.css`](styles.css) — Custom stylesheet providing modern responsive layouts, article card grids, and news sidebars.
- [`articles/`](articles/) — Individual article pages (`article-1.html` through `article-38.html`).
- [`videos/`](videos/) — Directory containing embedded article video reports (`video-1.mp4`, `video-10.mp4`, etc.).
- [`scripts/`](scripts/) — Veo video generation utilities, prompts (`scripts/prompts/`), parameters configuration ([`scripts/parameters.yaml`](scripts/parameters.yaml)), and generator script ([`scripts/generate_veo_videos.py`](scripts/generate_veo_videos.py)).
- [`requirements.txt`](requirements.txt) — Python dependencies for the Veo video generator.
- [`.env.example`](.env.example) — Template for environment configuration.
- [`Dockerfile`](Dockerfile) — Container build configuration based on `nginx:alpine` listening on port `8080`.
- [`nginx.conf`](nginx.conf) — Custom Nginx server configuration route handler.
- [`.dockerignore`](.dockerignore) — Docker build context exclusion file.

---

## 🎬 Generating Veo Video Reports

The site includes an automated Python script to generate 8-second video reports using **Google Veo** via Vertex AI and Application Default Credentials (ADC).

### 1. Environment Setup

1. **Create and Activate a Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Authenticate with Google Cloud (Application Default Credentials)**:
   ```bash
   gcloud auth application-default login
   ```

4. *(Optional)* **Configure `.env`**:
   Copy `.env.example` to `.env` if you wish to override project or region defaults:
   ```bash
   cp .env.example .env
   ```

### 2. Running Video Generation

1. **Configure Parameters**:
   Edit parameters such as model, duration, aspect ratio, and region in [`scripts/parameters.yaml`](scripts/parameters.yaml).

2. **Edit Prompts**:
   Individual prompts are stored as `.md` files in `scripts/prompts/` (e.g., `01_quantum_computing.md`).

3. **Execute the Script**:
   ```bash
   python3 scripts/generate_veo_videos.py
   ```

4. **Output & Publishing**:
   - Generated MP4 files will be saved in `scripts/output/` (e.g., `generated_video_01.mp4`).
   - Rename the files as needed (e.g. `video-1.mp4`) and move them into the [`videos/`](videos/) folder to serve them on the website.

---

## 🚀 Running Locally

### Option 1: Docker (Recommended)

1. **Build the Container Image**:
   ```bash
   docker build -t bmm-news-site .
   ```

2. **Run the Container**:
   ```bash
   docker run -d -p 8080:8080 --name bmm-news-site bmm-news-site
   ```

3. **View in Browser**:
   Open [http://localhost:8080](http://localhost:8080) in your web browser.

---

### Option 2: Local Web Server

Run a simple local HTTP server from the project directory:

```bash
# Using Python
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

---

## ☁️ Deploying to Google Cloud Run

This repository supports direct source-based deployments using Google Cloud Build and Cloud Run.

### Prerequisites

- [Google Cloud SDK (`gcloud` CLI)](https://cloud.google.com/sdk/docs/install) installed and authenticated.
- Active GCP Project (e.g. `bmm-news-site`) with the following APIs enabled:
  - **Cloud Run Admin API** (`run.googleapis.com`)
  - **Cloud Build API** (`cloudbuild.googleapis.com`)
  - **Artifact Registry API** (`artifactregistry.googleapis.com`)

### Deployment Command

Run the following command in the project root:

```bash
gcloud run deploy bmm-news-site \
  --source . \
  --project bmm-news-site \
  --region us-central1 \
  --allow-unauthenticated
```

Upon completion, Cloud Run will output the public service URL (e.g., `https://bmm-news-site-159619652659.us-central1.run.app`).

---

## 🔐 Service Account IAM Permissions

When using Cloud Build source-based deployment, ensure the Default Compute Service Account (`<PROJECT_NUMBER>-compute@developer.gserviceaccount.com`) has the following permissions:

- `roles/storage.objectViewer`
- `roles/logging.logWriter`
- `roles/artifactregistry.writer`
- `roles/cloudbuild.builds.builder`

To grant permissions via `gcloud`:
```bash
gcloud projects add-iam-policy-binding bmm-news-site \
  --member="serviceAccount:<PROJECT_NUMBER>-compute@developer.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"
```

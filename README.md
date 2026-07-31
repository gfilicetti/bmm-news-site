# BMM News Site

**BMM - The Most Trusted Brand in News**

A fast, responsive, containerized static news website showcasing breaking news, world headlines, and featured articles. The application is served using Nginx and optimized for deployment on **Google Cloud Run**.

---

## 📁 Repository Structure

- [`index.html`](index.html) — Main homepage featuring breaking news tickers, lead stories, story grids, and top headlines.
- [`styles.css`](styles.css) — Custom stylesheet providing modern responsive layouts, article card grids, and news sidebars.
- [`articles/`](articles/) — Individual article pages (`article-1.html` through `article-38.html`).
- [`videos/`](videos/) — Directory containing embedded article video reports (`video-1.mp4`, `video-10.mp4`, etc.).
- [`scripts/`](scripts/) — Deployment and video generation utilities:
  - [`scripts/deploy_cloud_run.sh`](scripts/deploy_cloud_run.sh) — Automated deployment script for Google Cloud Run.
  - [`scripts/run_local_docker.sh`](scripts/run_local_docker.sh) — Local Docker build and execution script.
  - [`scripts/grant_iam_permissions.sh`](scripts/grant_iam_permissions.sh) — Script to grant required Cloud Build IAM permissions.
  - [`scripts/generate_veo_videos.py`](scripts/generate_veo_videos.py) — Veo AI video generator script.
  - [`scripts/parameters.yaml.example`](scripts/parameters.yaml.example) — Parameters configuration template.
  - [`scripts/requirements.txt`](scripts/requirements.txt) — Python dependencies for video generation.
  - `scripts/prompts/` — Individual `.md` prompt files.
  - `scripts/output/` — Output folder for generated MP4 video files.
- [`.env.example`](.env.example) — Environment configuration template file.
- [`Dockerfile`](Dockerfile) — Container build configuration based on `nginx:alpine` listening on port `8080`.
- [`nginx.conf`](nginx.conf) — Custom Nginx server configuration route handler.
- [`.dockerignore`](.dockerignore) — Docker build context exclusion file.

---

## ⚙️ Environment Configuration

Copy the example template `.env.example` to `.env` to define your project settings:

```bash
cp .env.example .env
```

Edit `.env` with your deployment variables:
```env
GCP_PROJECT_ID=my-project-id
GCP_REGION=us-central1
SERVICE_NAME=my-app
```

> [!NOTE]
> `.env` is listed in `.gitignore` and will never be committed to source control.

---

## 🚀 Running Locally

### Option 1: Automated Script (Recommended)

Run the local Docker build script:
```bash
./scripts/run_local_docker.sh
```

View the application in your browser at [http://localhost:8080](http://localhost:8080).

---

### Option 2: Manual Docker Commands

1. **Build Container**:
   ```bash
   docker build -t my-app .
   ```

2. **Run Container**:
   ```bash
   docker run -d -p 8080:8080 --name my-app my-app
   ```

---

### Option 3: Local Web Server

Run a simple local HTTP server:
```bash
python3 -m http.server 8080
```

---

## ☁️ Deploying to Google Cloud Run

### Prerequisites

- [Google Cloud SDK (`gcloud` CLI)](https://cloud.google.com/sdk/docs/install) installed and authenticated.
- Active GCP Project with the following APIs enabled:
  - **Cloud Run Admin API** (`run.googleapis.com`)
  - **Cloud Build API** (`cloudbuild.googleapis.com`)
  - **Artifact Registry API** (`artifactregistry.googleapis.com`)

### Option 1: Automated Script (Recommended)

Deploy directly using your `.env` configuration:
```bash
./scripts/deploy_cloud_run.sh
```

### Option 2: Manual `gcloud` Command

```bash
gcloud run deploy my-app \
  --source . \
  --project my-project-id \
  --region us-central1 \
  --allow-unauthenticated
```

Upon completion, Cloud Run will output your public service URL (e.g., `https://my-app-xxxxxx.us-central1.run.app`).

---

## 🔐 Service Account IAM Permissions

When using Cloud Build source-based deployment, ensure the Default Compute Service Account (`<PROJECT_NUMBER>-compute@developer.gserviceaccount.com`) has the following permissions:

- `roles/storage.objectViewer`
- `roles/logging.logWriter`
- `roles/artifactregistry.writer`
- `roles/cloudbuild.builds.builder`

### Option 1: Automated IAM Script

Grant required permissions automatically using your `.env` settings:
```bash
./scripts/grant_iam_permissions.sh
```

### Option 2: Manual Command

```bash
gcloud projects add-iam-policy-binding my-project-id \
  --member="serviceAccount:<PROJECT_NUMBER>-compute@developer.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"
```

---

## 🎬 Generating Veo Video Reports (Vertex AI ADC)

The site includes an automated Python script to generate 8-second video reports using **Google Veo** via Vertex AI and Application Default Credentials (ADC).

### 1. Environment & Setup

1. **Create Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r scripts/requirements.txt
   ```

3. **Authenticate Application Default Credentials (ADC)**:
   ```bash
   gcloud auth application-default login
   ```

### 2. Running Video Generation

1. **Copy Parameters Template**:
   ```bash
   cp scripts/parameters.yaml.example scripts/parameters.yaml
   ```

2. **Configure GCP Project & Region**:
   Set your GCP `project` and `location` in `scripts/parameters.yaml`:
   ```yaml
   project: "my-project-id"
   location: "us-central1"
   model: "veo-3.1-lite-generate-001"
   ```

3. **Execute the Generator**:
   ```bash
   python3 scripts/generate_veo_videos.py
   ```

4. **Output & Publishing**:
   - Generated MP4 files are saved in `scripts/output/` (e.g., `generated_video_01.mp4`).
   - Rename the files as needed (e.g. `video-1.mp4`) and move them into [`videos/`](videos/) to serve them on the website.

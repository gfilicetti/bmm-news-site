#!/usr/bin/env bash
# Grant required Cloud Build IAM permissions to default compute service account

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load .env if present
if [ -f "$REPO_ROOT/.env" ]; then
    echo "Loading environment configuration from .env..."
    export $(grep -v '^#' "$REPO_ROOT/.env" | xargs)
elif [ -f "$REPO_ROOT/.env.example" ]; then
    echo "Warning: .env file not found. Falling back to .env.example..."
    export $(grep -v '^#' "$REPO_ROOT/.env.example" | xargs)
fi

PROJECT_ID="${GCP_PROJECT_ID:-my-project-id}"

if [ "$PROJECT_ID" = "my-project-id" ]; then
    echo "Error: Please set GCP_PROJECT_ID in your .env file."
    echo "Copy .env.example to .env and edit your variables:"
    echo "    cp .env.example .env"
    exit 1
fi

echo "Fetching project number for $PROJECT_ID..."
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

echo "=========================================="
echo "Granting IAM Permissions"
echo "  Project ID:      $PROJECT_ID"
echo "  Project Number:  $PROJECT_NUMBER"
echo "  Service Account: $SERVICE_ACCOUNT"
echo "=========================================="

ROLES=(
    "roles/storage.objectViewer"
    "roles/logging.logWriter"
    "roles/artifactregistry.writer"
    "roles/cloudbuild.builds.builder"
)

for ROLE in "${ROLES[@]}"; do
    echo "Granting role: $ROLE..."
    CLOUDSDK_METRICS_ENVIRONMENT=datacloud.antigravity gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="serviceAccount:$SERVICE_ACCOUNT" \
        --role="$ROLE" > /dev/null
done

echo "IAM permissions granted successfully for $SERVICE_ACCOUNT."

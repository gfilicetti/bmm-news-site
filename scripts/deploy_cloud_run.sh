#!/usr/bin/env bash
# Deploy to Google Cloud Run using configuration from .env

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
REGION="${GCP_REGION:-us-central1}"
SERVICE="${SERVICE_NAME:-my-app}"

if [ "$PROJECT_ID" = "my-project-id" ]; then
    echo "Error: Please set GCP_PROJECT_ID in your .env file."
    echo "Copy .env.example to .env and edit your variables:"
    echo "    cp .env.example .env"
    exit 1
fi

echo "=========================================="
echo "Deploying Cloud Run Service"
echo "  Project:  $PROJECT_ID"
echo "  Region:   $REGION"
echo "  Service:  $SERVICE"
echo "=========================================="

cd "$REPO_ROOT"

CLOUDSDK_METRICS_ENVIRONMENT=datacloud.antigravity gcloud run deploy "$SERVICE" \
    --source . \
    --project "$PROJECT_ID" \
    --region "$REGION" \
    --allow-unauthenticated

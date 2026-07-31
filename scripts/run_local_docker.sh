#!/usr/bin/env bash
# Build and run Docker container locally using configuration from .env

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

SERVICE="${SERVICE_NAME:-my-app}"

echo "=========================================="
echo "Building and Running Local Docker Container"
echo "  Container Image: $SERVICE"
echo "  Local Port:      8080"
echo "=========================================="

cd "$REPO_ROOT"

# Stop and remove existing container if running
docker stop "$SERVICE" 2>/dev/null || true
docker rm "$SERVICE" 2>/dev/null || true

echo "Building Docker image..."
docker build -t "$SERVICE" .

echo "Starting container on http://localhost:8080..."
docker run -d -p 8080:8080 --name "$SERVICE" "$SERVICE"

echo "Container '$SERVICE' is running! Open http://localhost:8080 in your browser."

#!/bin/bash

# Fail on any error
set -e

# Variables
PROJECT_ID="chatterfix-ui"
REGION="us-central1"
SERVICE_NAME="agent-core-ui"
IMAGE="us-central1-docker.pkg.dev/$PROJECT_ID/cloud-run-source-deploy/$SERVICE_NAME"

# Authenticate if necessary (uncomment and set your key path)
# gcloud auth activate-service-account --key-file="/path/to/key.json"

# Build Docker image
docker build -t $IMAGE -f deploy/Dockerfile .

# Push to Artifact Registry
docker push $IMAGE

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image=$IMAGE \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --port=8080

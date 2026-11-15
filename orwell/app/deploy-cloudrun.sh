#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-banercorp-web}"
REGION="${CLOUD_RUN_REGION:-northamerica-northeast2}"
SERVICE_NAME="${SERVICE_NAME:-orwell}"
MODEL="${GEMINI_MODEL:-gemini-3.8-flash}"

echo "Deploying Orwell to Google Cloud Run..."
echo "   Project : ${PROJECT_ID}"
echo "   Region  : ${REGION}"
echo "   Service : ${SERVICE_NAME}"
echo "   Model   : ${MODEL} (Vertex AI)"

gcloud run deploy "${SERVICE_NAME}" \
  --source . \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=global,GEMINI_MODEL=${MODEL}"

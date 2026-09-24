#!/usr/bin/env bash
# ==============================================================================
# Script: setup_bq_ml.sh
# Purpose: Configures BigQuery Cloud Resource Connection, Remote Gemini Model,
#          and the extracted_insights target table for the RAG pipeline.
# ==============================================================================

set -euo pipefail

if [ -z "${1:-}" ] || [ -z "${2:-}" ] || [ -z "${3:-}" ]; then
  echo "Usage: ./setup_bq_ml.sh <gcp_project_id> <gcp_region> <bq_dataset_id>"
  exit 1
fi

PROJECT_ID="$1"
REGION="$2"
DATASET_ID="$3"

echo "=================================================="
echo "Configuring BigQuery Remote LLM & Insights Table"
echo "Project: ${PROJECT_ID}"
echo "Region:  ${REGION}"
echo "Dataset: ${DATASET_ID}"
echo "=================================================="

# 1. Create Cloud Resource Connection
echo "Step 1: Creating Cloud Resource Connection..."
bq query --use_legacy_sql=false --project_id="${PROJECT_ID}" --location="${REGION}" \
"CREATE CONNECTION IF NOT EXISTS \`${PROJECT_ID}.${REGION}.vertex_llm_conn\`
  OPTIONS (connection_type = 'CLOUD_RESOURCE');"

# 2. Retrieve Connection Service Account
echo "Step 2: Retrieving connection service account..."
CONNECTION_SA=$(bq show --connection --project_id="${PROJECT_ID}" --location="${REGION}" vertex_llm_conn --format=json | grep -o '"serviceAccountId": "[^"]*' | cut -d'"' -f4)

echo "Found Connection Service Account: ${CONNECTION_SA}"
echo "Granting 'roles/aiplatform.user' to connection service account..."
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${CONNECTION_SA}" \
  --role="roles/aiplatform.user" > /dev/null

echo "✅ Granted Vertex AI User role to BigQuery connection SA."

# 3. Create BigQuery Remote Model Wrapper
echo "Step 3: Creating Remote Gemini Model..."
bq query --use_legacy_sql=false --project_id="${PROJECT_ID}" --location="${REGION}" \
"CREATE OR REPLACE MODEL \`${DATASET_ID}.gemini_pro_remote\`
  REMOTE WITH CONNECTION \`${PROJECT_ID}.${REGION}.vertex_llm_conn\`
  OPTIONS (endpoint = 'gemini-2.5-pro');"

# 4. Create Destination Table
echo "Step 4: Initializing extracted_insights table..."
bq query --use_legacy_sql=false --project_id="${PROJECT_ID}" --location="${REGION}" \
"CREATE OR REPLACE TABLE \`${DATASET_ID}.extracted_insights\`
AS
SELECT session_id, timestamp, CAST(NULL AS STRING) AS global_insight
FROM \`${DATASET_ID}.sanitized_transcripts\`
LIMIT 0;"

echo "=================================================="
echo "✅ BigQuery Remote LLM connection and tables ready!"
echo "=================================================="

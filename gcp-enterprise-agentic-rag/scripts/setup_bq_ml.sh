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
CONNECTION_SA=$(bq --format=json show --connection --project_id="${PROJECT_ID}" --location="${REGION}" vertex_llm_conn | python3 -c "import json, sys; print(json.load(sys.stdin)['cloudResource']['serviceAccountId'])")

echo "Found Connection Service Account: ${CONNECTION_SA}"
echo "Granting 'roles/aiplatform.user' to connection service account..."
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${CONNECTION_SA}" \
  --role="roles/aiplatform.user" > /dev/null

echo "✅ Granted Vertex AI User role to BigQuery connection SA."
echo "Waiting 20 seconds for IAM policy propagation..."
sleep 20

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

# 5. Create Daily Insights Scheduled Query
echo "Step 5: Setting up Daily Insights Scheduled Query..."
INSIGHTS_QUERY="INSERT INTO \`${PROJECT_ID}.${DATASET_ID}.extracted_insights\`
  (session_id, timestamp, global_insight)
SELECT
  session_id,
  timestamp,
  ML.GENERATE_TEXT(
    MODEL \`${PROJECT_ID}.${DATASET_ID}.gemini_pro_remote\`,
    (
      SELECT
        CONCAT(
          'Instructions: Analyze the conversation transcript provided below in JSON format.\n',
          'Specifically look for user feedback keywords like \"correct\", \"wrong\", or \"remember\".\n',
          'If you find these words or implied system corrections, extract the valuable feedback and summarize them as explicit, general system rules.\n',
          'Do not refer to individual user actions, session specifics, or mention PII.\n',
          'CRITICAL: If no user keywords or system rules can be extracted from the transcript, respond with exactly the word NO_RULE_DETECTED and nothing else than:\n',
          'Transcript JSON:\n',
          anonymized_transcript
        ) AS prompt
      FROM
        \`${PROJECT_ID}.${DATASET_ID}.sanitized_transcripts\`
      WHERE
        timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
    ),
    STRUCT(TRUE AS flatten_json_output)
  )
FROM
  \`${PROJECT_ID}.${DATASET_ID}.sanitized_transcripts\`
WHERE
  timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
  AND ML.generate_text_llm_result IS NOT NULL
  AND ML.generate_text_llm_result != 'NO_RULE_DETECTED';"

bq mk --transfer_config \
  --project_id="${PROJECT_ID}" \
  --data_source=scheduled_query \
  --display_name="Daily Insights Extraction" \
  --target_dataset="${DATASET_ID}" \
  --params="{\"query\":\"${INSIGHTS_QUERY}\"}" \
  --schedule="every 24 hours" 2>/dev/null || echo "⚠️ Scheduled query already exists or requires BigQuery Data Transfer Service API."

echo "=================================================="
echo "✅ BigQuery Remote LLM connection, tables, and scheduled ETL ready!"
echo "=================================================="

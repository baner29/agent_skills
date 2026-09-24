# Phase 5: Privacy-Preserving Closed-Loop RAG Pipeline

This reference describes the streaming telemetry, Cloud DLP anonymization, BigQuery ML summarization, and Vertex AI Search integration.

## 1. Pub/Sub Topic & BigQuery Staging Tables

```bash
gcloud pubsub topics create agent-session-transcripts --project="<gcp_project_id>"
bq --location="<gcp_region>" mk --dataset "<gcp_project_id>:<bq_dataset_id>"

bq mk --table \
  --schema session_id:STRING,user_id:STRING,timestamp:TIMESTAMP,anonymized_transcript:STRING \
  "<bq_dataset_id>.sanitized_transcripts"
```

## 2. Cloud DLP Sanitization Cloud Function

Deploy the Cloud Function (Gen 2) triggered by the Pub/Sub topic to redact PII (names, emails, phones) before inserting into BigQuery:
```bash
gcloud functions deploy process-transcript-stream \
  --runtime=python311 \
  --region="<gcp_region>" \
  --trigger-topic=agent-session-transcripts \
  --entry-point=process_transcript_stream \
  --gen2 \
  --memory=512Mi \
  --project="<gcp_project_id>"
```
See full Cloud Function code in `assets/template_cf_main.py`.

## 3. BigQuery ML Remote Connection & Model Provisioning

Run the bundled script `scripts/setup_bq_ml.sh` or execute the following SQL:

```sql
-- 1. Create Cloud Resource connection for Vertex AI LLMs
CREATE CONNECTION IF NOT EXISTS `<gcp_project_id>.<gcp_region>.vertex_llm_conn`
  OPTIONS (connection_type = "CLOUD_RESOURCE");

-- 2. Define the remote Gemini model inside BigQuery
CREATE OR REPLACE MODEL `<bq_dataset_id>.gemini_pro_remote`
  REMOTE WITH CONNECTION `<gcp_project_id>.<gcp_region>.vertex_llm_conn`
  OPTIONS (endpoint = 'gemini-2.5-pro');

-- 3. Create target destination schema table for condensed knowledge units
CREATE OR REPLACE TABLE `<bq_dataset_id>.extracted_insights`
AS
SELECT session_id, timestamp, CAST(NULL AS STRING) AS global_insight
FROM `<bq_dataset_id>.sanitized_transcripts`
LIMIT 0;
```

> [!IMPORTANT]
> The internal service account created by `vertex_llm_conn` must be granted `roles/aiplatform.user` so BigQuery ML can execute predictions against Vertex AI.

## 4. Vertex AI Search (Discovery Engine) Integration

1. In Vertex AI Search & Conversation, create a new **Data Store** of type **BigQuery**.
2. Connect it to `<gcp_project_id>.<bq_dataset_id>.extracted_insights`.
3. Create a Search App and obtain the **Data Store ID**. Set `VERTEX_SEARCH_DATA_STORE_ID=<id>` in the environment.

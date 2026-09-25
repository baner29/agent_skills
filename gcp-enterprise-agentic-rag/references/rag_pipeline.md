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

## 4. Automated Daily Insight Extraction (Scheduled Query)

To continuously extract system knowledge and insights from `sanitized_transcripts` into `extracted_insights`, configure a BigQuery Scheduled Query running on a daily schedule:

```sql
INSERT INTO `<gcp_project_id>.<bq_dataset_id>.extracted_insights`
  (session_id, timestamp, global_insight)
SELECT
  session_id,
  timestamp,
  ML.GENERATE_TEXT(
    MODEL `<gcp_project_id>.<bq_dataset_id>.gemini_pro_remote`,
    (
      SELECT
        CONCAT(
          'Instructions: Analyze the conversation transcript provided below in JSON format.\n',
          'Specifically look for user feedback keywords like "correct", "wrong", or "remember".\n',
          'If you find these words or implied system corrections, extract the valuable feedback and summarize them as explicit, general system rules.\n',
          'Do not refer to individual user actions, session specifics, or mention PII.\n',
          'CRITICAL: If no user keywords or system rules can be extracted from the transcript, respond with exactly the word NO_RULE_DETECTED and nothing else than:\n',
          'Transcript JSON:\n',
          anonymized_transcript
        ) AS prompt
      FROM
        `<gcp_project_id>.<bq_dataset_id>.sanitized_transcripts`
      WHERE
        timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
    ),
    STRUCT(TRUE AS flatten_json_output)
  )
FROM
  `<gcp_project_id>.<bq_dataset_id>.sanitized_transcripts`
WHERE
  timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
  AND ML.generate_text_llm_result IS NOT NULL
  AND ML.generate_text_llm_result != 'NO_RULE_DETECTED';
```

Create the scheduled transfer configuration:
```bash
bq mk --transfer_config \
  --project_id="<gcp_project_id>" \
  --data_source=scheduled_query \
  --display_name="Daily Insights Extraction" \
  --target_dataset="<bq_dataset_id>" \
  --params='{"query":"<INSERT_SQL_ABOVE>"}' \
  --schedule="every 24 hours"
```

## 5. Vertex AI Search (Discovery Engine) Integration

To enable RAG search across global sanitized transcripts and insights:

### Option A: Automated Provisioning via Script
Run the bundled script to create the Data Store and Search App automatically:
```bash
python scripts/setup_vertex_search.py \
  --project="<gcp_project_id>" \
  --dataset="<bq_dataset_id>" \
  --table="sanitized_transcripts"
```
Record the resulting `VERTEX_SEARCH_DATA_STORE_ID` in `.env`.

### Option B: Manual Provisioning via Google Cloud Console
If organization policies require UI approval or manual creation:
1. **Open AI Applications**: Navigate to **Vertex AI** > **Agent Builder** (or **Search & Conversation**) in Google Cloud Console.
2. **Create Search App**:
   - Click **Create App**.
   - Select **Custom Search (General)** option and click **Create**.
   - Check **Enterprise Edition features** and **Generative Responses**.
   - Enter your **App name** and **External Name of your company**.
   - Select **Global** for the app location, and click **Continue**.
3. **Create BigQuery Data Store**:
   - On the Data store page, click **Create Data store**.
   - Select **BigQuery** as the data source.
   - Under *Structured Data Import*, select **BigQuery table with your own schema**.
   - Under *Synchronization Frequency*, select **Periodic** (default: daily).
   - Under *Select a dataset you want to import*, choose `<bq_dataset_id>` (e.g. `global_agent_knowledge`), and for table select `sanitized_transcripts` (or `extracted_insights`).
   - Click **Continue**.
   - Enter your **Data store name** and select **General Pricing**.
   - Click **Create**.
4. **Link Data Store & Finalize App**:
   - Select the newly created data store and click **Continue**.
   - Select **General Pricing** for the search app and click **Create**.
5. **Update Environment**:
   - Locate and copy the **Data Store ID** (or Search App ID).
   - Set `VERTEX_SEARCH_DATA_STORE_ID=<data_store_id>` in `.env`.

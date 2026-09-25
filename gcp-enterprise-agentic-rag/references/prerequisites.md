# Phase 2: GCP Pre-Requisite Setup & Infrastructure

This reference details the GCP cloud APIs, IAM permissions, service account setup, and coding agent tools needed before deploying the multi-agent system.

## 1. Required GCP APIs

The following APIs must be enabled on the target GCP project:

```bash
gcloud services enable \
    aiplatform.googleapis.com \
    pubsub.googleapis.com \
    dlp.googleapis.com \
    bigquery.googleapis.com \
    bigqueryconnection.googleapis.com \
    cloudfunctions.googleapis.com \
    run.googleapis.com \
    discoveryengine.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    cloudresourcemanager.googleapis.com \
    iam.googleapis.com \
    logging.googleapis.com \
    monitoring.googleapis.com \
    cloudtrace.googleapis.com \
    eventarc.googleapis.com \
    eventarcpublishing.googleapis.com \
    --project="<gcp_project_id>"
```

## 2. Dedicated Service Account & Least-Privilege IAM Roles

Create the dedicated service account:
```bash
gcloud iam service-accounts create "<service_account_name>" \
    --display-name="<app_name> Agent Service Account" \
    --project="<gcp_project_id>"
```

Assign the required least-privilege IAM roles:
* `roles/aiplatform.user` (Vertex AI prediction, Agent Engine, and session/memory operations)
* `roles/bigquery.dataEditor` + `roles/bigquery.jobUser` (BigQuery dataset operations & query execution)
* `roles/pubsub.publisher` (Asynchronous event emission from agent callbacks)
* `roles/pubsub.subscriber` (Cloud Function event trigger consumption)
* `roles/dlp.user` (De-identifying PII in session transcripts)
* `roles/discoveryengine.editor` (Vertex AI Search indexing and querying)
* `roles/storage.objectAdmin` (Artifact staging and GCS-backed session storage)
* `roles/cloudtrace.agent` (Exporting OpenTelemetry traces)
* `roles/logging.logWriter` (Cloud Logging)

```bash
SA_EMAIL="<service_account_name>@<gcp_project_id>.iam.gserviceaccount.com"
for ROLE in \
    roles/aiplatform.user \
    roles/bigquery.dataEditor \
    roles/bigquery.jobUser \
    roles/pubsub.publisher \
    roles/pubsub.subscriber \
    roles/dlp.user \
    roles/discoveryengine.editor \
    roles/storage.objectAdmin \
    roles/cloudtrace.agent \
    roles/logging.logWriter; do
  gcloud projects add-iam-policy-binding "<gcp_project_id>" \
      --member="serviceAccount:${SA_EMAIL}" \
      --role="${ROLE}"
done
```

### Cloud Function Gen 2 Builder Role
For Cloud Functions Gen 2 triggered by Pub/Sub, grant `roles/cloudbuild.builds.builder` to the default compute service account:
```bash
PROJECT_NUMBER=$(gcloud projects describe "<gcp_project_id>" --format="value(projectNumber)")
gcloud projects add-iam-policy-binding "<gcp_project_id>" \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.builder"
```

## 3. Recommended Coding Agent Tooling

When executing within an MCP-capable coding assistant (such as Claude Code, Codex, Cursor, or Antigravity), equip the following tools:
* **MCP Servers**:
  - `bigquery`: Direct database inspection, schema querying, and query validation.
  - `github-mcp-server`: Codebase exploration, branch management, and PR automation.
  - `google-cloud-logging`: Real-time inspection of Cloud Function and Agent Runtime logs.
  - `google-cloud-monitoring`: Performance and quota monitoring.
  - `google-developer-knowledge` / `adk-docs-mcp`: Official Google ADK and Vertex AI SDK documentation.
* **Plugins / Extensions**:
  - Google Antigravity / Vertex AI SDK extensions
  - Gemini API integration plugins

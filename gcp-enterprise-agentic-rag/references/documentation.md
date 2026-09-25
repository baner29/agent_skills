# Phase 8: Application Documentation & GCP Console Playground Guide

After successfully deploying and verifying the multi-agent system on Vertex AI Agent Runtime, the coding agent must generate a comprehensive `README.md` in the root of the newly created application project.

This ensures developers and operators understand the internal mechanics, how to invoke the agent programmatically, and how to test it interactively using the GCP Console Playground.

---

## 1. Required Sections in the Generated Application `README.md`

The generated `README.md` must be tailored to the specific application created during the discovery interview and must include:

### 1.1 Project Title & Overview
- Name of the application and high-level mission.
- Description of `root_agent` and each specialized sub-agent (responsibilities, models used, and tools attached).

### 1.2 Architecture & How It Works
- **Orchestration Flow**: How `root_agent` receives user inputs, references past turns via `VertexAiSessionService`, accesses cross-session knowledge via `VertexAiMemoryBankService`, and delegates tasks to domain sub-agents.
- **Closed-Loop RAG**: How `after_agent_callback` streams session transcripts to Cloud Pub/Sub, sanitizes PII with Cloud DLP, summarizes insights using BigQuery ML remote Gemini models, and indexes them in Vertex AI Search.
- **Observability**: How OpenTelemetry traces are automatically captured and exported to Google Cloud Trace.

### 1.3 Local Environment & Prerequisites
- Required environment variables in `.env`:
  ```bash
  GOOGLE_CLOUD_PROJECT=<project_id>
  GOOGLE_CLOUD_REGION=<region>
  GOOGLE_CLOUD_MODEL=gemini-2.5-flash
  STORAGE_BUCKET=<staging_bucket>
  AGENT_ENGINE_ID=<deployed_agent_engine_id>
  SERVICE_NAME=<service_name>
  VERTEX_SEARCH_DATA_STORE_ID=<data_store_id>
  ```
- Dependencies and installation (`pip install -r requirements.txt`).

### 1.4 Deployment & Maintenance Commands
- Creating or updating the Agent Engine instance:
  ```bash
  # Deploy or update deployment on Vertex AI Agent Runtime
  python deploy_agent_engine.py --mode=update --engine_id=<engine_id>
  ```

---

## 2. Interactive Testing via GCP Console Playground

The documentation must provide explicit, step-by-step instructions for testing the agent in the Google Cloud Console:

### Step-by-Step Navigation
1. **Log in to GCP Console**: Navigate to [Google Cloud Console](https://console.cloud.google.com/).
2. **Select Target Project**: Ensure the active project matches `GOOGLE_CLOUD_PROJECT`.
3. **Open Vertex AI Agent Engine**:
   - In the navigation menu, go to **Vertex AI** > **Agent Builder** (or **Agent Engine**).
   - In the list of deployed agents/engines, click on the deployed service: `<service_name>` (Engine ID: `AGENT_ENGINE_ID`).
4. **Access the Playground**:
   - In the agent details page, click on the **Playground** tab in the top or side navigation panel.
5. **Interactive Testing & Validation**:
   - **Multi-Turn Conversation**: Type test queries related to the sub-agents' domains. Observe how `root_agent` triages and invokes the appropriate sub-agent tool.
   - **Inspect Tool Calls**: Expand the turn drawer in the playground UI to view real-time sub-agent tool invocations, inputs, and intermediate outputs.
   - **Memory & Session Verification**: Send a preference or fact (e.g., *"I prefer concise bullet points with schema names in uppercase"*), start a new turn or session, and verify that the agent recalls the stored preference via `PreloadMemoryTool`.
   - **Cloud Trace Inspection**: Click the **Trace** or **View in Cloud Trace** link in the playground to inspect execution waterfall spans, model latencies, and token counts.

---

## 3. Programmatic Invocation (SDK & API)

Provide sample code in the `README.md` showing how client applications can invoke the deployed agent:

```python
import vertexai
from vertexai import agent_engines

vertexai.init(project="<gcp_project_id>", location="<gcp_region>")

# Retrieve the deployed Agent Engine
engine = agent_engines.get("<agent_engine_id>")

# Create a new session for the user
session = engine.create_session(user_id="user_123")

# Send a query and stream the response
response_stream = engine.stream_query(
    message="Show me the database trends from last week",
    user_id="user_123",
    session_id=session["id"]
)

for event in response_stream:
    if isinstance(event, dict) and "content" in event:
        parts = event["content"].get("parts", [])
        for part in parts:
            if "text" in part:
                print(part["text"], end="", flush=True)
print()
```

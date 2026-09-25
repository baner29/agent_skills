# Phase 1: Requirements Discovery Interview

Before generating any code or executing commands, the coding agent (Claude Code, Codex, Cursor, Antigravity, or others) must interview the user to collect project-specific requirements.

> [!NOTE]
> The root orchestrator agent name is standardized to **`root_agent`** across all templates, so there is no need to ask the user to name it.

## Discovery Questionnaire

Ask the user the following structured questions:

1. **Application Name**: The display and service name for the agent (e.g., `technical-knowledge-agent`, `customer-support-agent`).
2. **Number of Sub-Agents**: Total count of specialized domain sub-agents needed.
3. **Sub-Agent Profiles & Tool Access**: For each sub-agent:
   - Name of the sub-agent (e.g., `database_analyst`, `repository_searcher`, `documentation_agent`, `ticketing_agent`).
   - Brief domain responsibility and instructions (e.g., "Analyzes relational schemas and runs diagnostic queries").
   - Tool capabilities required (e.g., BigQuery querying/schema introspection, GitHub repository code search, Vertex AI Search, Jira/ticketing APIs, file parsing).
4. **Google Cloud Project ID**: Target GCP Project ID (e.g., `my-company-prod-ai`).
5. **Google Cloud Region / Location**: Target region for compute and Vertex AI services (Default: `europe-west1` or `us-central1`).
6. **Cloud Storage Staging Bucket**: GCS bucket for Agent Runtime artifacts and session persistence (e.g., `<app-name>-staging-<project-id>`).
7. **Service Account**: Existing Service Account email to execute the agent, or permission to create a new dedicated one (e.g., `<app-name>-sa@<project-id>.iam.gserviceaccount.com`).
8. **Global Knowledge Base (RAG) Dataset**: BigQuery dataset name for sanitized session transcripts and extracted insights (Default: `global_agent_knowledge`).
9. **LLM Model**: Model identifier to power the agents (Default: `gemini-2.5-flash`).
   - *Notice: Ensure the chosen model is available and supported in the specified GCP region.*
10. **Interface Adapter Preferences**: Desired user entrypoints (e.g., GCP console agent playground, Google Chat Webhook, Slack bot, lightweight web chat adapter).

---

## Pre-Flight Regional Model Check

Prior to generating code or scaffolding the project, the agent must verify that the selected model is active and accessible in the target region by executing a minimal test generation:

```bash
python3 -c "from google import genai; client = genai.Client(vertexai=True, project='<gcp_project_id>', location='<gcp_region>'); client.models.generate_content(model='<model_id>', contents='ping')"
```

If the endpoint returns `404 NOT_FOUND`, notify the user immediately and select an available model for that region (e.g., `gemini-2.5-flash`).


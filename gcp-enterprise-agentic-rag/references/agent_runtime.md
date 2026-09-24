# Phase 6: Vertex AI Agent Runtime Deployment

This reference details provisioning and deploying the Google ADK multi-agent application on the managed Vertex AI Agent Runtime (Agent Engine).

## 1. Provision Agent Engine Instance

Execute `create_engine.py`:
```python
import vertexai

client = vertexai.Client(project="<gcp_project_id>", location="<gcp_region>")
agent_engine = client.agent_engines.create()
engine_id = agent_engine.api_resource.name.split("/")[-1]
print(f"AGENT_ENGINE_ID={engine_id}")
```
Add `AGENT_ENGINE_ID=<engine_id>` to `.env`.

## 2. Deploy via `AdkApp`

Run `deploy_agent_engine.py`:
```bash
python deploy_agent_engine.py --mode=create
```

Key configuration points in `deploy_agent_engine.py`:
* **Tracing Enabled**: `adk_app = AdkApp(app=app, session_service_builder=..., memory_service_builder=..., enable_tracing=True)`
* **OpenTelemetry Environment Flags**:
  - `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY="true"`
  - `OTEL_SEMCONV_STABILITY_OPT_IN="gen_ai_latest_experimental"`
  - `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT="EVENT_ONLY"`
  - `GOOGLE_GENAI_USE_VERTEXAI="1"`
* **Packaging**: Pass `extra_packages=["./root_agent"]` and `requirements="requirements.txt"` to `agent_engines.create()` or `agent_engines.get().update()`.

See full deployment script in `assets/template_deploy.py`.

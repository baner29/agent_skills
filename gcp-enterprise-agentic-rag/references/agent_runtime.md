# Phase 6: Vertex AI Agent Runtime Deployment

This reference details provisioning and deploying the Google ADK multi-agent application on the managed Vertex AI Agent Runtime (Agent Engine).

## 1. Two-Phase Deployment Lifecycle

`VertexAiMemoryBankService` and `VertexAiSessionService` require `AGENT_ENGINE_ID` during instantiation. Deployments must follow a two-phase workflow:

### Phase A: Provision Empty Agent Engine Instance
Execute `create_engine.py` to create the managed engine container and obtain its unique ID:
```python
import vertexai

client = vertexai.Client(project="<gcp_project_id>", location="<gcp_region>")
agent_engine = client.agent_engines.create()
engine_id = agent_engine.api_resource.name.split("/")[-1]
print(f"AGENT_ENGINE_ID={engine_id}")
```
Persist `AGENT_ENGINE_ID=<engine_id>` into `.env`.

### Phase B: Package & Update Engine with Application Code
Deploy the application package to the provisioned engine:
```bash
python deploy_agent_engine.py --mode=update --engine_id=<engine_id>
```

---

## 2. Configuration & Packaging Standards

Key implementation requirements in `deploy_agent_engine.py`:
* **Tracing Enabled**: `adk_app = AdkApp(app=app, session_service_builder=session_service_builder, memory_service_builder=memory_service_builder, enable_tracing=True)`
* **Non-Empty Environment Variables**: Vertex AI Reasoning Engine rejects environment variables set to empty strings. Filter out empty keys:
  ```python
  env_vars = {k: v for k, v in env_vars.items() if v}
  ```
* **Required OpenTelemetry Environment Flags**:
  - `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY="true"`
  - `OTEL_SEMCONV_STABILITY_OPT_IN="gen_ai_latest_experimental"`
  - `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT="EVENT_ONLY"`
  - `GOOGLE_GENAI_USE_VERTEXAI="1"`
* **Packaging**: Pass `extra_packages=["./root_agent"]` and `requirements="requirements.txt"` (which must include `cloudpickle>=3.0.0`) to `agent_engines.get(engine_id).update()`.

See full deployment script in `assets/template_deploy.py`.

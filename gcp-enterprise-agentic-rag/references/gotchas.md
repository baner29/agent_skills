# Gotchas & Critical Edge Cases

This reference documents non-obvious GCP environment behaviors and edge cases.

## 1. BigQuery Connection Service Account Permission
Creating the `vertex_llm_conn` Cloud Resource connection generates an internal Google service account.
- **Problem**: Running `ML.GENERATE_TEXT` yields an `Access Denied` or `IAM permission missing` error.
- **Solution**: You must grant this service account `roles/aiplatform.user`. The bundled script `scripts/setup_bq_ml.sh` extracts the service account ID and binds the role automatically.

## 2. Memory Service Garbage Collection Bug Workaround
In Google ADK memory generation callbacks:
```python
await callback_context.add_events_to_memory(
    events=callback_context.session.events,
    custom_metadata={"wait_for_completion": False}
)
```
- **Problem**: Asynchronous background tasks during agent shutdown can lead to the client session being prematurely closed or garbage collected.
- **Solution**: Setting `wait_for_completion=False` in `custom_metadata` tells the service to dispatch event extraction without blocking the agent's turn return or dropping the callback context.

## 3. Sub-Agent Session Isolation
- **Problem**: If sub-agents share the root agent's unpartitioned session history, large SQL schemas or repository search payloads quickly saturate the root agent's LLM context window.
- **Solution**: Always isolate sub-agent execution turns, or pass scoped sub-session IDs (e.g. `{session_id}-{sub_agent_name}`) so sub-agent intermediate tokens stay within the sub-agent boundary.

## 4. Cloud DLP Region Compatibility
- **Problem**: Cloud DLP inspect and deidentify requests can fail if there is a mismatch between the regional endpoint and the project location.
- **Solution**: Ensure the Cloud Function triggers and Cloud DLP client requests use the same regional configuration.

## 5. OpenTelemetry GenAI Stability Opt-In
- **Problem**: Detailed Gemini spans, tool invocations, and token counts do not appear in Google Cloud Trace.
- **Solution**: Pass `OTEL_SEMCONV_STABILITY_OPT_IN="gen_ai_latest_experimental"` and `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT="EVENT_ONLY"` into the Agent Engine environment variables.

## 6. Vertex AI Reasoning Engine Empty Environment Variables
- **Problem**: Deploying an engine with empty string environment variables fails with `Field: reasoning_engine.spec.deployment_spec.env[i].value; Message: Required field is not set.`
- **Solution**: Strip empty strings from the `env_vars` dictionary (`{k: v for k, v in env_vars.items() if v}`) before calling `create` or `update`.

## 7. BigQuery Connection Service Account IAM Latency
- **Problem**: Attempting to execute `CREATE MODEL ... REMOTE WITH CONNECTION` immediately after granting `roles/aiplatform.user` fails with authorization errors.
- **Solution**: GCP IAM cache synchronization requires a 15-20 second propagation window. Add a wait period after binding IAM roles.

## 8. `AdkApp.stream_query` Parameter Contract
- **Problem**: Remote calls to `stream_query` fail with `TypeError: AdkApp.stream_query() missing 2 required keyword-only arguments: 'message' and 'user_id'`.
- **Solution**: Ensure client invocations pass `message`, `user_id`, and `session_id` as keyword arguments.

## 9. Cloud Functions Gen 2 Cloud Build Permissions
- **Problem**: Deploying Gen 2 Cloud Functions with Pub/Sub triggers prompts for missing Eventarc APIs and Cloud Build builder permissions.
- **Solution**: Ensure `eventarc.googleapis.com` and `eventarcpublishing.googleapis.com` are enabled, and `roles/cloudbuild.builds.builder` is assigned to `${PROJECT_NUMBER}-compute@developer.gserviceaccount.com`.

## 10. `cloudpickle` Serialization Dependency
- **Problem**: Packaging `AdkApp` into `agent_engine.pkl` fails with `No package metadata was found for cloudpickle`.
- **Solution**: Always include `cloudpickle>=3.0.0` in `requirements.txt`.


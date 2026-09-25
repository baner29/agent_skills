# Phase 3: Project Scaffolding & Agent Architecture

This reference outlines the multi-agent code layout, ADK session service, persistent memory bank, and root orchestrator wiring.

## 1. Directory Layout

```text
<app_name>/
├── .env
├── requirements.txt
├── create_engine.py
├── deploy_agent_engine.py
├── process-transcript-stream-cf/
│   ├── main.py
│   └── requirements.txt
├── root_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── rag_integration.py
│   └── <sub_agent_1>/
│       ├── __init__.py
│       └── agent.py
│   └── <sub_agent_2>/
│       ├── __init__.py
│       └── agent.py
```

## 2. Requirements (`requirements.txt`)

```text
google-adk>=0.1.0
google-genai>=0.1.0
google-cloud-aiplatform>=1.70.0
google-cloud-bigquery>=3.20.0
google-cloud-pubsub>=2.20.0
google-cloud-dlp>=3.15.0
google-cloud-discoveryengine>=0.11.0
opentelemetry-api>=1.20.0
python-dotenv>=1.0.0
pydantic>=2.0.0
requests>=2.28.0
cloudpickle>=3.0.0
```

## 3. State & Memory Service Builders (`root_agent/agent.py`)

```python
import os
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
from google.adk.agents.callback_context import CallbackContext

def session_service_builder():
    """Builds per-turn GCS-backed session service for Agent Engine."""
    return VertexAiSessionService(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        location=os.environ.get("GOOGLE_CLOUD_REGION", "us-central1"),
        agent_engine_id=os.environ.get("AGENT_ENGINE_ID"),
    )

def memory_service_builder():
    """Builds persistent cross-session memory bank service."""
    return VertexAiMemoryBankService(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        location=os.environ.get("GOOGLE_CLOUD_REGION", "us-central1"),
        agent_engine_id=os.environ.get("AGENT_ENGINE_ID"),
    )

async def generate_memories_callback(callback_context: CallbackContext):
    """Triggers memory extraction across turns."""
    if callback_context.session:
        # Note: wait_for_completion=False prevents background client garbage collection
        await callback_context.add_events_to_memory(
            events=callback_context.session.events,
            custom_metadata={"wait_for_completion": False}
        )
    return None
```

## 4. Root Orchestrator & Sub-Agent Wiring

```python
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.adk.tools import FunctionTool

root_agent = Agent(
    name="root_agent",
    model=os.environ.get("GOOGLE_CLOUD_MODEL", "gemini-2.5-flash"),
    instruction="""You are the root orchestrator. Triage user requests and delegate to specialized sub-agents. 
Do not execute heavy queries or code searches directly; delegate to the domain expert. 
Synthesize clear, direct answers for the user.""",
    tools=[
        PreloadMemoryTool(),
        FunctionTool(search_global_knowledge_base)
    ],
    sub_agents=[sub_agent_1, sub_agent_2],
    after_agent_callback=[generate_memories_callback, stream_to_global_rag_pipeline]
)

app = App(name="<app_name>", root_agent=root_agent)
```
See full starter code in `assets/template_agent.py`.

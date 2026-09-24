"""
Template: root_agent/agent.py
Description: Production-ready Google ADK Multi-Agent Orchestrator with Vertex AI 
             Session & Memory Bank integration and closed-loop RAG hooks.
"""

import os
import json
import logging
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools import FunctionTool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
from google.adk.agents.callback_context import CallbackContext
from google.cloud import pubsub_v1
from google.cloud import discoveryengine_v1beta as discoveryengine

load_dotenv()
logger = logging.getLogger(__name__)

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("PROJECT_ID")
REGION = os.environ.get("GOOGLE_CLOUD_REGION", "europe-west1")
MODEL_NAME = os.environ.get("GOOGLE_CLOUD_MODEL", "gemini-3.8-flash")
AGENT_ENGINE_ID = os.environ.get("AGENT_ENGINE_ID")
DATA_STORE_ID = os.environ.get("VERTEX_SEARCH_DATA_STORE_ID")

# ==============================================================================
# 1. Vertex AI Session & Memory Service Builders
# ==============================================================================

def session_service_builder():
    """Builds per-turn GCS-backed session service for Agent Engine."""
    return VertexAiSessionService(
        project=PROJECT_ID,
        location=REGION,
        agent_engine_id=AGENT_ENGINE_ID,
    )

def memory_service_builder():
    """Builds persistent cross-session memory bank service."""
    return VertexAiMemoryBankService(
        project=PROJECT_ID,
        location=REGION,
        agent_engine_id=AGENT_ENGINE_ID,
    )

async def generate_memories_callback(callback_context: CallbackContext):
    """Asynchronously triggers memory extraction across turns."""
    if callback_context.session:
        await callback_context.add_events_to_memory(
            events=callback_context.session.events,
            custom_metadata={"wait_for_completion": False}
        )
    return None

# ==============================================================================
# 2. Closed-Loop RAG Telemetry & Knowledge Search
# ==============================================================================

async def stream_to_global_rag_pipeline(callback_context: CallbackContext) -> None:
    """Streams conversation history to Pub/Sub for Cloud DLP anonymization and indexing."""
    try:
        session = callback_context._invocation_context.session
        if not session or not session.events:
            return

        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(PROJECT_ID, "agent-session-transcripts")

        payload = {
            "session_id": session.id,
            "user_id": getattr(session, "user_id", "anonymous"),
            "history": [
                {
                    "role": event.content.role if event.content else "unknown",
                    "text": "".join([part.text for part in event.content.parts if part.text])
                    if event.content and event.content.parts else ""
                }
                for event in session.events
            ]
        }
        publisher.publish(topic_path, json.dumps(payload).encode("utf-8"))
    except Exception as e:
        logger.warning(f"Telemetry stream failed safely: {e}")

def search_global_knowledge_base(query: str) -> str:
    """Searches historical insights and resolutions in Vertex AI Search."""
    if not DATA_STORE_ID:
        return "Knowledge base search is currently unconfigured."
    
    try:
        client = discoveryengine.SearchServiceClient()
        serving_config = client.serving_config_path(
            project=PROJECT_ID,
            location="global",
            data_store=DATA_STORE_ID,
            serving_config="default_search"
        )
        request = discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=query,
            page_size=3
        )
        response = client.search(request)
        snippets = []
        for result in response.results:
            data = result.document.derived_struct_data
            if "snippets" in data and data["snippets"]:
                snippets.append(data["snippets"][0].get("snippet", ""))
        
        if not snippets:
            return "No previous historical insights found for this query."
        return "\n[Historical Knowledge Base Insights]:\n" + "\n---\n".join(snippets)
    except Exception as e:
        logger.warning(f"Search failed: {e}")
        return "Knowledge base temporarily unavailable."

# ==============================================================================
# 3. Example Sub-Agent Definition (Add as many sub-agents as needed)
# ==============================================================================

# Example: Database Analysis Sub-Agent
def sample_db_tool(sql_query: str) -> str:
    """Execute SQL query against BigQuery (placeholder)."""
    return f"Simulated query execution for: {sql_query}"

sample_sub_agent = Agent(
    name="sample_sub_agent",
    model=MODEL_NAME,
    instruction="You are a specialist sub-agent. Handle domain-specific queries and return concise answers.",
    tools=[FunctionTool(sample_db_tool), FunctionTool(search_global_knowledge_base)],
    after_agent_callback=[stream_to_global_rag_pipeline]
)

# ==============================================================================
# 4. Root Orchestrator Definition
# ==============================================================================

root_agent = Agent(
    name="root_agent",
    model=MODEL_NAME,
    instruction="""You are the root orchestrator agent.
Your primary role is to understand user queries and delegate them to the appropriate specialized sub-agent.
- Do not perform heavy database queries or technical code searches yourself; delegate to your sub-agents.
- Use past preferences from memory to personalize responses.
- Synthesize sub-agent outputs into clear, actionable responses for the user.""",
    tools=[
        PreloadMemoryTool(),
        FunctionTool(search_global_knowledge_base)
    ],
    sub_agents=[sample_sub_agent],
    after_agent_callback=[generate_memories_callback, stream_to_global_rag_pipeline]
)

# Application Wrapper
app = App(
    name=os.environ.get("SERVICE_NAME", "enterprise_agent"),
    root_agent=root_agent
)

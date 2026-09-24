"""
Template: deploy_agent_engine.py
Description: Deploys or updates the ADK Multi-Agent application on Vertex AI Agent Runtime (Agent Engine).
"""

import os
import sys
import argparse
import vertexai
from vertexai import agent_engines
from vertexai.agent_engines.templates.adk import AdkApp
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "europe-west1")
STORAGE_BUCKET = os.environ.get("STORAGE_BUCKET")
SERVICE_NAME = os.environ.get("SERVICE_NAME", "enterprise_agent_adk")
AGENT_ENGINE_ID = os.environ.get("AGENT_ENGINE_ID")
SERVICE_ACCOUNT = os.environ.get("AGENT_ENGINE_SERVICE_ACCOUNT")

def parse_args():
    parser = argparse.ArgumentParser(description="Deploy or update ADK Agent on Vertex AI Agent Runtime")
    parser.add_argument(
        "--mode",
        choices=["create", "update", "auto"],
        default="auto",
        help="Whether to create a new deployment, update existing, or auto-detect based on AGENT_ENGINE_ID",
    )
    parser.add_argument(
        "--engine_id",
        default=None,
        help="Specific Agent Engine ID to target (overrides AGENT_ENGINE_ID env var)",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    target_engine_id = args.engine_id or AGENT_ENGINE_ID

    print("=" * 60)
    print("VERTEX AI AGENT RUNTIME DEPLOYMENT")
    print("=" * 60)
    print(f"Project:        {PROJECT_ID}")
    print(f"Location:       {LOCATION}")
    print(f"Staging Bucket: gs://{STORAGE_BUCKET}")
    print(f"Engine ID:      {target_engine_id or 'Not set'}")
    print("=" * 60)

    # Initialize Vertex AI SDK
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=f"gs://{STORAGE_BUCKET}",
    )

    # Import root_agent app and builders
    print("\n[1/4] Loading root_agent application...")
    from root_agent.agent import app, session_service_builder, memory_service_builder

    # Wrap in Vertex AI AdkApp template with OpenTelemetry Tracing enabled
    print("[2/4] Packaging into AdkApp template with OpenTelemetry enabled...")
    adk_app = AdkApp(
        app=app,
        session_service_builder=session_service_builder,
        memory_service_builder=memory_service_builder,
        enable_tracing=True,
    )

    # Environment variables required by the Agent Runtime
    env_vars = {
        "PROJECT_ID": PROJECT_ID,
        "GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY": "true",
        "OTEL_SEMCONV_STABILITY_OPT_IN": "gen_ai_latest_experimental",
        "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT": "EVENT_ONLY",
        "GOOGLE_GENAI_USE_VERTEXAI": "1",
        "GOOGLE_CLOUD_REGION": LOCATION,
        "STORAGE_BUCKET": STORAGE_BUCKET,
        "GOOGLE_CLOUD_MODEL": os.environ.get("GOOGLE_CLOUD_MODEL", "gemini-3.8-flash"),
        "SERVICE_NAME": SERVICE_NAME,
        "AGENT_ENGINE_ID": target_engine_id or "",
    }

    # Pass through optional keys if present
    for opt_key in ["VERTEX_SEARCH_DATA_STORE_ID", "GITHUB_TOKEN"]:
        val = os.environ.get(opt_key)
        if val:
            env_vars[opt_key] = val

    extra_packages = ["./root_agent"]
    requirements = "requirements.txt"

    mode = args.mode
    if mode == "auto":
        mode = "update" if target_engine_id else "create"

    print(f"\n[3/4] Preparing deployment (Mode: {mode})...")

    try:
        if mode == "update" and target_engine_id:
            print(f"Updating existing Agent Engine: {target_engine_id}...")
            remote_engine = agent_engines.get(target_engine_id)
            updated_engine = remote_engine.update(
                agent_engine=adk_app,
                requirements=requirements,
                extra_packages=extra_packages,
                env_vars=env_vars,
                display_name=SERVICE_NAME,
                service_account=SERVICE_ACCOUNT,
            )
            engine_id = updated_engine.resource_name.split("/")[-1]
            print(f"\n✅ SUCCESS! Updated Agent Engine: {engine_id}")
        else:
            print(f"Creating new Agent Engine: {SERVICE_NAME}...")
            created_engine = agent_engines.create(
                agent_engine=adk_app,
                requirements=requirements,
                extra_packages=extra_packages,
                env_vars=env_vars,
                display_name=SERVICE_NAME,
                description="Enterprise Multi-Agent System on Vertex AI Agent Runtime",
                service_account=SERVICE_ACCOUNT,
            )
            engine_id = created_engine.resource_name.split("/")[-1]
            print(f"\n✅ SUCCESS! Created new Agent Engine: {engine_id}")
            print(f"Resource Name: {created_engine.resource_name}")
            print(f"\nPlease ensure AGENT_ENGINE_ID={engine_id} is saved in your .env file.")

    except Exception as e:
        print(f"\n❌ Deployment error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

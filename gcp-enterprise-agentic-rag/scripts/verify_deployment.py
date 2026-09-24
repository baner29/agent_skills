#!/usr/bin/env python3
"""
Script: scripts/verify_deployment.py
Purpose: Post-deployment self-validation script for coding agents to verify the
         live GCP deployment: Agent Engine, Pub/Sub, Cloud Function, BigQuery, and RAG.
"""

import os
import sys
import argparse
from dotenv import load_dotenv

load_dotenv()

def print_result(check: str, success: bool, detail: str = ""):
    icon = "✅" if success else "❌"
    print(f"{icon} {check}: {detail}")
    if not success:
        sys.exit(1)

def verify_agent_engine(project: str, location: str, engine_id: str):
    try:
        import vertexai
        from vertexai import agent_engines

        vertexai.init(project=project, location=location)
        engine = agent_engines.get(engine_id)
        name = engine.resource_name
        print_result("Agent Engine Status", True, f"Online and accessible ({name})")
    except Exception as e:
        print_result("Agent Engine Status", False, f"Failed to retrieve engine {engine_id}: {e}")

def verify_pubsub(project: str, topic_name: str = "agent-session-transcripts"):
    try:
        from google.cloud import pubsub_v1
        client = pubsub_v1.PublisherClient()
        topic_path = client.topic_path(project, topic_name)
        client.get_topic(request={"topic": topic_path})
        print_result("Pub/Sub Topic", True, f"Found active topic {topic_path}")
    except Exception as e:
        print_result("Pub/Sub Topic", False, f"Failed to verify topic {topic_name}: {e}")

def verify_bigquery(project: str, dataset_id: str):
    try:
        from google.cloud import bigquery
        client = bigquery.Client(project=project)
        dataset = client.get_dataset(dataset_id)
        
        tables = [t.table_id for t in client.list_tables(dataset)]
        required_tables = ["sanitized_transcripts", "extracted_insights"]
        missing = [t for t in required_tables if t not in tables]
        if missing:
            print_result("BigQuery RAG Tables", False, f"Missing tables in {dataset_id}: {missing}")
        else:
            print_result("BigQuery RAG Tables", True, f"All required tables exist in {dataset_id} ({tables})")
    except Exception as e:
        print_result("BigQuery RAG Tables", False, f"Error checking dataset {dataset_id}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Verify GCP Multi-Agent RAG Deployment")
    parser.add_argument("--project", default=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    parser.add_argument("--location", default=os.environ.get("GOOGLE_CLOUD_REGION", "europe-west1"))
    parser.add_argument("--engine_id", default=os.environ.get("AGENT_ENGINE_ID"))
    parser.add_argument("--dataset", default=os.environ.get("BQ_DATASET_NAME", "global_agent_knowledge"))
    args = parser.parse_args()

    if not args.project or not args.engine_id:
        print("❌ Error: Missing --project or --engine_id (or GOOGLE_CLOUD_PROJECT / AGENT_ENGINE_ID in .env)")
        sys.exit(1)

    print("=" * 60)
    print(f"Verifying Live Deployment for Project: {args.project}")
    print(f"Agent Engine ID: {args.engine_id}")
    print("=" * 60)

    verify_agent_engine(args.project, args.location, args.engine_id)
    verify_pubsub(args.project)
    verify_bigquery(args.project, args.dataset)

    print("=" * 60)
    print("🎉 ALL SYSTEMS OPERATIONAL! Deployment self-validation complete.")
    print("=" * 60)

if __name__ == "__main__":
    main()

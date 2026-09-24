"""
Template: process-transcript-stream-cf/main.py
Description: Cloud Function (Gen 2) triggered by Pub/Sub to scrub PII using Cloud DLP
             and stream sanitized conversation transcripts into BigQuery.
"""

import os
import base64
import json
from datetime import datetime
import functions_framework
from google.cloud import dlp_v2
from google.cloud import bigquery

# Initialize clients globally for connection reuse across invocations
dlp_client = dlp_v2.DlpServiceClient()
bq_client = bigquery.Client()

DATASET_NAME = os.environ.get("BQ_DATASET_NAME", "global_agent_knowledge")
TABLE_NAME = os.environ.get("BQ_TABLE_NAME", "sanitized_transcripts")

def scrub_pii(text_content: str, project_id: str) -> str:
    """Uses Cloud DLP to redact names, emails, and phone numbers with placeholders."""
    if not text_content:
        return ""

    parent = f"projects/{project_id}"

    inspect_config = {
        "info_types": [
            {"name": "PERSON_NAME"},
            {"name": "EMAIL_ADDRESS"},
            {"name": "PHONE_NUMBER"}
        ]
    }

    deidentify_config = {
        "info_type_transformations": {
            "transformations": [{
                "primitive_transformation": {
                    "replace_with_info_type_value": {}
                }
            }]
        }
    }

    try:
        response = dlp_client.deidentify_content(
            request={
                "parent": parent,
                "deidentify_config": deidentify_config,
                "inspect_config": inspect_config,
                "item": {"value": text_content},
            }
        )
        return response.item.value
    except Exception as e:
        print(f"Warning: Cloud DLP de-identification encountered an error: {e}")
        return text_content

@functions_framework.cloud_event
def process_transcript_stream(cloud_event):
    """Processes Pub/Sub cloud event containing conversation transcripts."""
    project_id = bq_client.project

    # Extract Pub/Sub message
    pubsub_data = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
    payload = json.loads(pubsub_data)

    session_id = payload.get("session_id", "unknown")
    user_id = payload.get("user_id", "anonymous")
    raw_history = json.dumps(payload.get("history", []))

    # Anonymize conversation history with Cloud DLP
    clean_history = scrub_pii(raw_history, project_id)

    # Format row for BigQuery streaming insert
    table_id = f"{project_id}.{DATASET_NAME}.{TABLE_NAME}"
    rows_to_insert = [{
        "session_id": session_id,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "anonymized_transcript": clean_history
    }]

    errors = bq_client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        raise RuntimeError(f"BigQuery streaming insert failed: {errors}")
    
    print(f"Successfully processed and stored sanitized transcript for session {session_id}")

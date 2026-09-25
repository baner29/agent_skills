#!/usr/bin/env python3
"""
Script: setup_vertex_search.py
Purpose: Automates the creation of a Vertex AI Search Data Store and Search Engine (App)
         connected to the BigQuery global knowledge dataset, or prints manual console fallback steps.
"""

import sys
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Setup Vertex AI Search Data Store and App for BigQuery")
    parser.add_argument("--project", required=True, help="Google Cloud Project ID")
    parser.add_argument("--location", default="global", help="Location for Discovery Engine (default: global)")
    parser.add_argument("--dataset", required=True, help="BigQuery Dataset ID (e.g. global_agent_knowledge)")
    parser.add_argument("--table", default="sanitized_transcripts", help="BigQuery Table ID (e.g. sanitized_transcripts or extracted_insights)")
    parser.add_argument("--data_store_id", default=None, help="Custom Data Store ID (defaults to <dataset>-store)")
    parser.add_argument("--engine_id", default=None, help="Custom Engine/App ID (defaults to <dataset>-search-app)")
    return parser.parse_args()

def main():
    args = parse_args()
    project_id = args.project
    location = args.location
    dataset_id = args.dataset
    table_id = args.table
    data_store_id = args.data_store_id or f"{dataset_id.replace('_', '-')}-store"
    engine_id = args.engine_id or f"{dataset_id.replace('_', '-')}-search-app"

    print("=" * 60)
    print("VERTEX AI SEARCH & DATA STORE SETUP")
    print("=" * 60)
    print(f"Project ID:      {project_id}")
    print(f"Location:        {location}")
    print(f"BigQuery Table:  {project_id}.{dataset_id}.{table_id}")
    print(f"Data Store ID:   {data_store_id}")
    print(f"Search App ID:   {engine_id}")
    print("=" * 60)

    try:
        from google.cloud import discoveryengine_v1beta as discoveryengine

        # 1. Initialize Clients
        ds_client = discoveryengine.DataStoreServiceClient()
        parent_collection = f"projects/{project_id}/locations/{location}/collections/default_collection"

        # 2. Create Data Store
        print("\n[1/3] Creating Vertex AI Search Data Store...")
        try:
            data_store = discoveryengine.DataStore(
                display_name=f"{dataset_id.replace('_', ' ').title()} Store",
                industry_vertical=discoveryengine.IndustryVertical.GENERIC,
                solution_types=[discoveryengine.SolutionType.SOLUTION_TYPE_SEARCH],
                content_config=discoveryengine.DataStore.ContentConfig.STRUCTURED,
            )
            op = ds_client.create_data_store(
                parent=parent_collection,
                data_store=data_store,
                data_store_id=data_store_id,
            )
            print("Waiting for Data Store creation to complete...")
            op.result(timeout=180)
            print(f"✅ Created Data Store: {data_store_id}")
        except Exception as e:
            if "AlreadyExists" in str(e) or "already exists" in str(e):
                print(f"ℹ️ Data Store {data_store_id} already exists.")
            else:
                raise e

        # 3. Import BigQuery Table Documents
        print(f"\n[2/3] Importing BigQuery Table {dataset_id}.{table_id}...")
        try:
            doc_client = discoveryengine.DocumentServiceClient()
            parent_branch = f"projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{data_store_id}/branches/0"
            bigquery_source = discoveryengine.BigQuerySource(
                project_id=project_id,
                dataset_id=dataset_id,
                table_id=table_id,
                data_schema="custom",
            )
            import_req = discoveryengine.ImportDocumentsRequest(
                parent=parent_branch,
                bigquery_source=bigquery_source,
                reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
            )
            import_op = doc_client.import_documents(request=import_req)
            print("Import initiated successfully.")
        except Exception as e:
            print(f"⚠️ BigQuery import notice: {e}")

        # 4. Create Search Engine (App)
        print("\n[3/3] Creating Search Engine (App)...")
        try:
            engine_client = discoveryengine.EngineServiceClient()
            search_engine = discoveryengine.Engine(
                display_name=f"{dataset_id.replace('_', ' ').title()} Search App",
                solution_type=discoveryengine.SolutionType.SOLUTION_TYPE_SEARCH,
                search_engine_config=discoveryengine.Engine.SearchEngineConfig(
                    search_tier=discoveryengine.SearchTier.SEARCH_TIER_ENTERPRISE,
                    search_add_ons=[discoveryengine.SearchAddOn.SEARCH_ADD_ON_LLM],
                ),
                data_store_ids=[data_store_id],
            )
            engine_op = engine_client.create_engine(
                parent=parent_collection,
                engine=search_engine,
                engine_id=engine_id,
            )
            engine_op.result(timeout=180)
            print(f"✅ Created Search App: {engine_id}")
        except Exception as e:
            if "AlreadyExists" in str(e) or "already exists" in str(e):
                print(f"ℹ️ Search App {engine_id} already exists.")
            else:
                raise e

        print("\n" + "=" * 60)
        print("✅ SUCCESS: Vertex AI Search Data Store and App ready!")
        print(f"VERTEX_SEARCH_DATA_STORE_ID={data_store_id}")
        print("=" * 60)
        return 0

    except Exception as e:
        print(f"\n⚠️ Automated setup encountered an issue: {e}")
        print("\n" + "=" * 60)
        print("MANUAL FALLBACK STEPS (Google Cloud Console):")
        print("=" * 60)
        print("1. Navigate to: Vertex AI > Agent Builder / Search & Conversation in GCP Console.")
        print("2. Click 'Create App' -> Select 'Custom Search (General)'.")
        print("3. Check 'Enterprise Edition features' & 'Generative Responses'.")
        print("4. Provide App Name and Company Name, set Location to 'Global', click Continue.")
        print("5. On Data Store page, click 'Create Data Store' -> Select 'BigQuery'.")
        print("6. Under Structured Data Import: Select 'BigQuery table with your own schema'.")
        print("7. Under Synchronization: Select 'Periodic' (Daily).")
        print(f"8. Under Dataset: Select '{dataset_id}', Table: Select '{table_id}'.")
        print(f"9. Complete Data Store creation and note the Data Store ID.")
        print("10. Set VERTEX_SEARCH_DATA_STORE_ID=<data_store_id> in .env and redeploy.")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())

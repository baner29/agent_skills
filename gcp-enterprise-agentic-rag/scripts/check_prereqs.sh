#!/usr/bin/env bash
# ==============================================================================
# Script: check_prereqs.sh
# Purpose: Validates GCP prerequisites, authentication, APIs, and IAM roles.
# ==============================================================================

set -euo pipefail

if [ -z "${1:-}" ]; then
  echo "Usage: ./check_prereqs.sh <gcp_project_id> [service_account_email]"
  exit 1
fi

PROJECT_ID="$1"
SA_EMAIL="${2:-}"

echo "=================================================="
echo "Checking GCP Prerequisites for Project: ${PROJECT_ID}"
echo "=================================================="

# 1. Check gcloud CLI
if ! command -v gcloud &> /dev/null; then
  echo "❌ Error: gcloud CLI is not installed."
  exit 1
fi
echo "✅ gcloud CLI installed."

# 2. Check active auth
ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
if [ -z "$ACTIVE_ACCOUNT" ]; then
  echo "❌ Error: No active gcloud authentication found. Run 'gcloud auth login'."
  exit 1
fi
echo "✅ Authenticated as: ${ACTIVE_ACCOUNT}"

# 3. Check Required APIs
REQUIRED_APIS=(
  "aiplatform.googleapis.com"
  "pubsub.googleapis.com"
  "dlp.googleapis.com"
  "bigquery.googleapis.com"
  "bigqueryconnection.googleapis.com"
  "cloudfunctions.googleapis.com"
  "run.googleapis.com"
  "discoveryengine.googleapis.com"
  "artifactregistry.googleapis.com"
  "cloudbuild.googleapis.com"
  "cloudresourcemanager.googleapis.com"
  "iam.googleapis.com"
  "logging.googleapis.com"
  "monitoring.googleapis.com"
  "cloudtrace.googleapis.com"
  "eventarc.googleapis.com"
  "eventarcpublishing.googleapis.com"
)

echo "Checking required APIs..."
ENABLED_SERVICES=$(gcloud services list --enabled --project="${PROJECT_ID}" --format="value(config.name)")

MISSING_APIS=()
for api in "${REQUIRED_APIS[@]}"; do
  if ! echo "$ENABLED_SERVICES" | grep -q "^${api}$"; then
    MISSING_APIS+=("$api")
  fi
done

if [ ${#MISSING_APIS[@]} -gt 0 ]; then
  echo "⚠️ The following APIs are missing. Enabling them now:"
  for api in "${MISSING_APIS[@]}"; do
    echo "  - $api"
  done
  gcloud services enable "${MISSING_APIS[@]}" --project="${PROJECT_ID}"
  echo "✅ All required APIs enabled."
else
  echo "✅ All required APIs are already enabled."
fi

# 4. Check & Grant Cloud Build builder role to default compute SA
PROJECT_NUMBER=$(gcloud projects describe "${PROJECT_ID}" --format="value(projectNumber)")
COMPUTE_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
echo "Ensuring Cloud Build builder role on compute SA: ${COMPUTE_SA}..."
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${COMPUTE_SA}" \
  --role="roles/cloudbuild.builds.builder" > /dev/null 2>&1 || true
echo "✅ Cloud Build builder role verified."

# 5. Check Service Account if provided
if [ -n "$SA_EMAIL" ]; then
  echo "Checking service account existence: ${SA_EMAIL}..."
  if ! gcloud iam service-accounts describe "${SA_EMAIL}" --project="${PROJECT_ID}" &>/dev/null; then
    SA_NAME=$(echo "$SA_EMAIL" | cut -d'@' -f1)
    echo "Creating service account: ${SA_NAME}..."
    gcloud iam service-accounts create "${SA_NAME}" \
      --display-name="Agent Service Account" \
      --project="${PROJECT_ID}"
    echo "✅ Created service account: ${SA_EMAIL}"
  else
    echo "✅ Service account exists."
  fi

  echo "Checking IAM bindings for: ${SA_EMAIL}..."
  PROJECT_POLICY=$(gcloud projects get-iam-policy "${PROJECT_ID}" --format=json)
  REQUIRED_ROLES=(
    "roles/aiplatform.user"
    "roles/bigquery.dataEditor"
    "roles/bigquery.jobUser"
    "roles/pubsub.publisher"
    "roles/pubsub.subscriber"
    "roles/dlp.user"
    "roles/discoveryengine.editor"
    "roles/storage.objectAdmin"
    "roles/cloudtrace.agent"
    "roles/logging.logWriter"
  )

  for role in "${REQUIRED_ROLES[@]}"; do
    if echo "$PROJECT_POLICY" | grep -q "\"role\": \"${role}\""; then
      echo "  ✅ ${role}"
    else
      echo "  ⚠️ Missing ${role}. Granting..."
      gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
        --member="serviceAccount:${SA_EMAIL}" \
        --role="${role}" > /dev/null
      echo "  ✅ Granted ${role}"
    fi
  done
fi

echo "=================================================="
echo "Pre-requisite check completed successfully!"
echo "=================================================="

# Operational Runbook: Zero-Downtime PostgreSQL 14 to 16 Migration

This document provides step-by-step technical procedures for migrating production Cloud SQL PostgreSQL 14 instances to PostgreSQL 16 using read-replica cross-version upgrades.

## Audience & Purpose
- **Intended Audience**: Database Administrators, Senior DevOps Engineers, and On-Call SREs.
- **Purpose**: Upgrade production databases without user-facing downtime or data loss.

## Safety Notices

> [!CAUTION]
> **DANGER: Irreversible Data Loss Hazard**
> Executing the replica promotion command while replication lag is greater than 0 bytes will cause permanent data loss of uncommitted writes.
> **Required Action**: Confirm `Replication_Lag_Bytes == 0` before triggering replica promotion.

> [!WARNING]
> **WARNING: Extended Read-Only Mode**
> Placing the primary database into read-only mode prevents customer checkouts until promotion finishes.
> **Required Action**: Schedule this maintenance strictly during the off-peak maintenance window (02:00–04:00 UTC).

## Prerequisites
- [ ] Active GCP IAM role `roles/cloudsql.admin`.
- [ ] Cloud SDK CLI (`gcloud`) version >= 470.0.0 installed.
- [ ] Full logical backup verified:
  ```bash
  gcloud sql export sql prod-pg14-instance gs://prod-backups/pre-upgrade.sql --database=checkout_db
  ```

## Step-by-Step Procedure

### 1. Verify Replication Health
Execute replication lag query on replica:
```bash
gcloud sql instances describe prod-pg16-replica --format="value(replicaConfiguration.failoverTarget)"
```
> Expected output: `True`

### 2. Put Application into Maintenance Drain
Drain incoming API traffic:
```bash
kubectl scale deployment/checkout-api --replicas=0 -n production
```

### 3. Promote Read Replica to Master
Promote the PostgreSQL 16 instance to standalone master:
```bash
gcloud sql instances promote-replica prod-pg16-replica --quiet
```
> Expected output: `Promoting Cloud SQL instance... Done.`

### 4. Switch DNS Connection Endpoint
Update Secret Manager database hostname:
```bash
gcloud secrets versions add db-host --data-file=<(echo -n "10.0.4.50")
```

## Verification & Health Check
Verify application connectivity and write capability:
1. Restart checkout microservices:
   ```bash
   kubectl scale deployment/checkout-api --replicas=5 -n production
   ```
2. Execute health check HTTP endpoint:
   ```bash
   curl -f https://checkout.internal.corp/healthz
   ```
   > Expected output: `{"status":"HEALTHY","db_version":"PostgreSQL 16.2"}`

## Rollback & Troubleshooting
If promotion fails or schema incompatibilities occur:
1. Re-point `db-host` secret back to original PostgreSQL 14 IP (`10.0.4.20`).
2. Re-scale API pods: `kubectl rollout restart deployment/checkout-api -n production`.

# Operational Runbook: PostgreSQL 14 to 16 Migration with a Planned Write Pause

## Audience & Purpose

Database administrators and on-call SREs can adapt this example for a continuous Google Database Migration Service (DMS) migration to Cloud SQL PostgreSQL 16. It is a rehearsal template, not an executable production change plan. The application-specific controls below must be filled in and tested before use.

A write interruption is required at cutover. Strict zero downtime is not established by this procedure; if uninterrupted writes are mandatory, stop and design and test an application continuity strategy first.

## Prerequisites

- Record the project, region, source and destination instance identities, migration job, databases, operator, maintenance window, maximum write-pause duration, and abort deadline in the change plan.

- Verify support for the source, target version, extensions, and schema with the current DMS documentation. Use a tested continuous DMS job, not an assumed cross-version physical read replica.

- Complete a staging rehearsal and a backup restore drill. Record backup identifiers, restore results, retention, and recovery time; successful export alone is not a verified recovery path.

- Verify least-privilege access for the migration and connection change. Keep credentials out of the document.

- Resolve migration fidelity gaps: roles and grants, tables without primary keys, sequences, unsupported objects, extensions, scheduled jobs, and DDL changes. Freeze schema changes during cutover.

- Supply tested application-specific procedures for blocking new writes, draining transactions, stopping workers and schedulers, fencing source writers, changing connections, and restoring service. Record every connection consumer and its current configuration version.

- Keep application writers disconnected from the destination until cutover validation. Establish a single writable authority and a way to prove that the other database cannot receive application writes.

## Safety Notices

> [!CAUTION]
> **DANGER: Lost Writes or Divergent Databases**
> Promotion with unapplied changes can omit committed source transactions. Returning to the source after destination writes can lose those new changes.
> **Required Action**: Fence source writers, verify catch-up, and follow the rollback boundary below. Never allow both databases to accept application writes.

> [!WARNING]
> **WARNING: Checkout Write Interruption**
> Requests that need the database cannot complete normally during the cutover pause.
> **Required Action**: Use the agreed maintenance response or a tested durable queue with idempotent replay. Define timeout and abort criteria before the window; do not claim zero downtime.

## Step-by-Step Procedure

### 1. Verify the Migration and Prepare the Cutover

Open the selected DMS migration job in the recorded project and region. Confirm the source and destination identities, completed initial load, healthy CDC phase, and coverage of every intended database. Resolve replication errors before continuing.

Use the job's Replication delay chart and inspect its timestamp and database coverage. DMS exposes `migration_job/max_replica_bytes_lag` for outstanding log bytes. A configuration flag is not a lag measurement. Missing or stale telemetry is a failed gate, not zero lag.

### 2. Pause Writes and Fence the Source

Activate the rehearsed maintenance or durable-queue procedure. Stop all source application writes, scripts, workers, scheduled jobs, and application client connections; allow in-flight transactions to finish within the recorded deadline. Keep the DMS replication connection operational.

Use the tested database access fence to prevent old clients from reconnecting and writing. Verify no active or prepared application transactions remain and that a representative old application credential cannot write. Record the final committed application transaction markers for each migrated database.

Keep the API available for its tested maintenance response where supported. Scaling the API to zero is an outage, not a traffic-drain or write-fencing mechanism. If any writer cannot be fenced or the pause deadline expires, stop before promotion and use the pre-promotion abort path.

### 3. Verify Catch-Up After the Fence

Wait for fresh DMS replication-delay measurements of zero bytes covering the entire migration job and every included database after source writes have stopped. Check that CDC remains healthy and no database is omitted. Confirm final committed markers and the rehearsed data reconciliation checks on the destination.

Proceed only when the writer fence, current zero-lag evidence, and data checks all pass. Lag alone does not validate objects that DMS does not replicate. If telemetry is stale, missing, nonzero, or inconsistent with the data checks, do not promote.

### 4. Promote the DMS Migration

With all gates satisfied and the source still fenced, use **Promote** on the verified DMS job's details page. Promotion cannot be undone once started. Wait for job status **Completed**; a submitted operation is not proof of success.

If completion is uncertain, keep application writes blocked on both sides and inspect the job and destination state. Do not retry promotion or redirect traffic blindly. See [Google's promotion procedure](https://docs.cloud.google.com/database-migration/docs/postgres/promote-migration).

### 5. Change Connections and Validate Before Resuming Writes

Apply the rehearsed connection configuration change to the verified destination identity. Refresh or roll out every consumer as required by its actual secret-loading behavior, and retire old connection pools. Creating a secret version alone does not refresh running applications or change DNS.

Confirm each consumer reaches PostgreSQL 16 on the intended destination. Complete the recorded schema, permissions, data, and sequence checks before enabling writers. Verify destination backup and point-in-time recovery settings.

Record the first destination write, including any validation write or sequence adjustment, as the conservative boundary after which simple source failback is prohibited. Run the rehearsed transactional canary and enable traffic gradually only after its result is correct. Keep the source fenced.

## Verification & Health Check

- Confirm the destination identity and PostgreSQL major version through each application's real connection path.
- Verify a canary transaction can commit and be read back, with its expected business result and no duplicate side effects.
- Compare agreed data reconciliation results and final source transaction markers; an HTTP health response alone cannot establish data integrity.
- Monitor error rate, latency, connection failures, queue backlog, and transaction success against the change plan's acceptance thresholds for its full observation window.
- Confirm the source remains fenced, all consumers use the destination, and backups and recovery are configured and verified before declaring completion. Retain the source and migration evidence for the agreed recovery period.

## Rollback & Troubleshooting

| Observed state | Required response |
|---|---|
| Before promotion, source remains authoritative | Abort cutover. Keep destination application writers blocked, verify all clients still target the source, then remove the source fence and resume the original writer set through the rehearsed procedure. |
| Promotion running, failed, or outcome uncertain | Keep writes blocked. Determine actual migration and destination state with the DBA; do not assume the operation was undone. |
| Promotion completed, no destination writes | A controlled return to the source requires proof of no destination changes, destination fencing, and verification of every client connection before source writers resume. Rebuild or re-establish migration before a later retry. |
| Any destination writes, or uncertainty about writes | Do not simply repoint clients to the old source. Fence writes, preserve both databases and logs, and prefer repair on the destination. Returning requires a separately tested reconciliation or reverse-migration plan that accounts for every new transaction and schema/version compatibility. Obtain the incident owner's recovery decision before resuming a single writer. |

## Technical References

- [DMS replication-delay metrics and database coverage](https://docs.cloud.google.com/database-migration/docs/postgres/migration-job-metrics)
- [DMS migration limitations and object fidelity](https://docs.cloud.google.com/database-migration/docs/postgres/known-limitations)

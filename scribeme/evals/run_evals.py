#!/usr/bin/env python3
"""
run_evals.py: Evaluation runner for scribeme skill.
Executes test cases, generates sample technical documents, and evaluates
compliance against invisible scaffolding and anti-AI writing guardrails.
"""

import sys
import json
from pathlib import Path

# Add scripts directory to path to import doc_validator
SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
import doc_validator


SAMPLE_DOC_1_SYSTEM_SPEC = """# System Architecture Specification: Distributed Checkout Platform

This document specifies the technical architecture, domain boundaries, and transaction flows for the Distributed Checkout Platform.

## 1. Introduction and Goals
The Distributed Checkout Platform coordinates payment processing, customer order capture, and transactional notifications during peak commercial events.

### Top Quality Goals
1. **P99 Latency < 250ms**: End-to-end checkout processing time under peak load.
2. **Availability 99.95%**: Uninterrupted checkout capability across multi-region deployments.
3. **Auditability**: Complete end-to-end trace logs for every financial transaction.

### Stakeholder Requirements
| Stakeholder | Concern | Architectural Expectation |
|---|---|---|
| Product Manager | High conversion rate | Low cart abandonment from slow processing |
| Security Officer | PCI-DSS compliance | Tokenized payment processing with zero raw PAN storage |
| SRE Lead | System resilience | Self-healing pods with circuit breakers |

## 2. Architecture Constraints
- **Cloud Platform**: Google Cloud Platform (Cloud Run & Cloud SQL).
- **Compliance**: PCI-DSS Level 1 compliance; no cardholder data touches application memory.
- **Language Stack**: Go 1.22 for low-latency backend microservices.

## 3. Context and Scope
The system interfaces with shoppers on the web, internal fraud detection, Stripe for payment authorization, and SendGrid for transactional emails.

```mermaid
flowchart TD
    Customer["👤 Customer<br/>[Person]<br/>Places items in cart and checks out"]
    subgraph Boundary["Enterprise System Boundary"]
        Platform["📦 Checkout Platform<br/>[Software System]<br/>Orchestrates checkout, orders, and payments"]
    end
    Stripe["🏢 Stripe API<br/>[External System]<br/>Payment gateway"]
    SendGrid["🏢 SendGrid API<br/>[External System]<br/>Transactional email dispatcher"]

    Customer -->|"Submits order<br/>[HTTPS]"| Platform
    Platform -->|"Authorizes card token<br/>[REST / HTTPS]"| Stripe
    Platform -->|"Sends order confirmation<br/>[Webhook / HTTPS]"| SendGrid
```

## 4. Solution Strategy
- **Decoupled Asynchronous Processing**: Orders are authorized synchronously, but fulfillment and notification dispatch occur asynchronously via event streams.
- **Transactional Outbox**: Guaranteed event delivery using transactional outbox pattern to prevent split-brain states between the database and event bus.

## 5. Building Block View
Decomposition into container building blocks:

```mermaid
flowchart TD
    subgraph Containers["Checkout Subsystem"]
        API["⚙️ Checkout API<br/>[Container: Go / Gin]<br/>Handles web requests and token validation"]
        DB[("🗄️ Orders DB<br/>[Container: PostgreSQL]<br/>Stores order ledgers")]
        Queue["📨 Event Bus<br/>[Container: Kafka]<br/>Publishes domain events"]
        Worker["💼 Notification Worker<br/>[Container: Go Daemon]<br/>Consumes events and invokes email APIs"]
    end

    API -->|"Writes order records"| DB
    API -->|"Emits OrderPlaced event"| Queue
    Queue -->|"Consumes events"| Worker
```

## 6. Runtime View
The following sequence diagram details the checkout sequence:

```mermaid
sequenceDiagram
    autonumber
    actor C as 👤 Customer
    participant API as ⚙️ Checkout API
    participant Pay as 🏢 Stripe
    participant DB as 🗄️ PostgreSQL
    participant Bus as 📨 Kafka

    C->>API: POST /api/v1/orders (PaymentToken)
    activate API
    API->>Pay: Authorize payment ($49.99)
    Pay-->>API: 200 OK (ChargeID: ch_abc123)
    API->>DB: INSERT INTO orders (Status: CONFIRMED)
    API->>Bus: Emit OrderPlaced(OrderID: 101)
    API-->>C: 201 Created (OrderID: 101)
    deactivate API
```

## 7. Deployment View
Deployed across 3 GCP zones using serverless Cloud Run instances connected to a Cloud SQL High Availability PostgreSQL cluster via private VPC peering.

## 8. Crosscutting Concepts
- **Idempotency**: All payment API endpoints enforce unique `Idempotency-Key` headers stored in Redis.
- **Observability**: Distributed traces generated via OpenTelemetry exporter to Cloud Trace.

### Technical Requirement to User Outcome Translation
| Requirement | Technical Implementation | User & Business Outcome |
|---|---|---|
| **High Availability** | Multi-AZ Cloud SQL with automated failover | Shoppers can complete purchases even during a data center disruption. |
| **Throughput** | Asynchronous Kafka event routing | System sustains 5,000 orders/sec without slowing down the checkout UI. |
| **Security** | End-to-end tokenization via Stripe Elements | User financial credentials cannot be intercepted by compromised services. |

## 9. Architecture Decisions
- [ADR-001](file:///docs/adr/001-kafka-streaming.md): Asynchronous Event Streaming with Apache Kafka.
- [ADR-002](file:///docs/adr/002-stripe-tokenization.md): Client-side Payment Tokenization.

## 10. Quality Requirements
- **Stress Scenario**: When load surges to 10,000 req/sec, API autoscales within 45 seconds and maintains error rates below 0.01%.

## 11. Risks and Technical Debt
| Risk | Impact | Planned Mitigation |
|---|---|---|
| Stripe gateway rate limits | High | Implement exponential backoff retry policy with jitter |

## 12. Glossary
- **Idempotency Key**: Unique UUID provided by client to prevent duplicate charges.
- **Outbox Pattern**: Design pattern guaranteeing atomicity between database writes and message broker publishes.
"""


SAMPLE_DOC_2_ADR = """# ADR-001: Selection of Event Streaming Platform for Order Processing

- **Status**: Accepted
- **Date**: 2026-03-01
- **Deciders**: Systems Architect, Lead Backend Engineer, Principal SRE

## Context and Problem Statement
Our order processing platform currently relies on synchronous HTTP microservice calls. During peak flash sales, downstream inventory and reporting services become overwhelmed, causing request timeouts and blocking customer checkouts. We need an asynchronous event backbone to decouple order ingestion from downstream consumers.

## Decision Drivers
- High throughput requirement: Must sustain at least 50,000 events/second at peak.
- Strong ordering guarantee per customer partition.
- Long-term event replay capability for analytics and disaster recovery.
- Cloud deployment options and operational complexity.

## Considered Options
1. **Apache Kafka (Confluent Cloud / Strimzi)**
2. **RabbitMQ**
3. **AWS SQS / GCP Pub/Sub**

## Decision Outcome
Chosen option: **Apache Kafka**, because it provides distributed partitioned logs with strict ordering and durable offset replay.

### Decision Summary
> In the context of the distributed order processing platform,
> facing peak flash-sale loads exceeding 50,000 events per second,
> we decided for Apache Kafka,
> to achieve strictly ordered, persistent event streaming and decoupled consumer scaling,
> accepting higher operational cluster maintenance overhead.

---

## Trade-off Analysis Matrix

| Evaluation Criteria | Apache Kafka (Chosen) | RabbitMQ | GCP Pub/Sub |
|---|---|---|---|
| **Peak Throughput (>50k/sec)** | Exceeds 100k/sec | Degrades at 30k/sec | Managed auto-scale |
| **Strict Ordering per Key** | Partition key hashing | Complex setup | Ordering keys add lag |
| **Message Replay** | Offset rewinding | Destructive reads | Limited seek window |
| **Operational Overhead** | Moderate (Zookeeper/KRaft) | Low | Zero server management |
| **Estimated Monthly Cost** | $1,800 (Managed) | $900 | $2,400 at peak |

---

## Consequences & Mitigation
- **Positive**: Complete decoupling between checkout service and inventory/marketing listeners.
- **Positive**: Ability to replay event streams from 7 days ago if an analytics bug occurs.
- **Negative Trade-off**: Operational complexity of partition management and consumer rebalancing.
  - *Mitigation*: We will use managed GCP Kafka or Confluent Cloud to eliminate self-hosted ZooKeeper/KRaft maintenance.
  - *Mitigation*: Configure automated Prometheus alerts for consumer lag exceeding 10,000 records.
"""


SAMPLE_DOC_3_RUNBOOK = """# Operational Runbook: PostgreSQL 14 to 16 Migration with a Planned Write Pause

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
"""


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("==================================================")
    print("Starting scribeme Skill Evaluations")
    print("==================================================")

    evals_file = SKILL_ROOT / "evals" / "evals.json"
    with open(evals_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    test_samples = [
        ("eval-1-full-architecture-spec", SAMPLE_DOC_1_SYSTEM_SPEC),
        ("eval-2-adr-event-streaming", SAMPLE_DOC_2_ADR),
        ("eval-3-production-database-migration-runbook", SAMPLE_DOC_3_RUNBOOK)
    ]

    all_passed = True
    temp_dir = SKILL_ROOT / "evals" / "artifacts"
    temp_dir.mkdir(parents=True, exist_ok=True)

    for case_id, doc_content in test_samples:
        case_spec = next(c for c in data["eval_cases"] if c["id"] == case_id)
        doc_path = temp_dir / f"{case_id}.md"
        doc_path.write_text(doc_content, encoding="utf-8")

        print(f"\nEvaluating: {case_spec['title']} ({case_id})")
        print(f"Target Mode: {case_spec['target_mode']}")

        res = doc_validator.validate_document(doc_path)

        # Check required sections
        missing_sections = []
        for sec in case_spec.get("required_sections", []):
            if sec.lower() not in doc_content.lower():
                missing_sections.append(sec)

        if missing_sections:
            print(f"[FAIL] Missing required sections: {missing_sections}")
            all_passed = False
        else:
            print(f"[PASS] All {len(case_spec['required_sections'])} required sections found.")

        # Check doc_validator results
        if res.errors:
            print(f"[ERROR] Validation Errors: {res.errors}")
            all_passed = False
        else:
            print(f"[PASS] Structural Validator: 0 Errors (Diagrams: {res.metrics.get('mermaid_diagram_count', 0)}, Alerts: {res.metrics.get('safety_alert_count', 0)})")

        if res.warnings:
            print(f"[WARN] Validation Warnings: {res.warnings}")

    # Negative Test Verification: Confirm that methodology meta-text and standard citations are blocked
    print("\n--------------------------------------------------")
    print("Running Negative-Test Assertions (Ensuring Guardrails Block Forbidden Patterns)")
    print("--------------------------------------------------")
    negative_sample = """# Payment Service Architecture
This documentation suite reflects the system implementation directly from the source code. All configuration values, API contracts, database schemas, and operational parameters correspond to active production code.
Follows the Lean arc42 framework and C4 Model Level 2 container specifications.
Operational runbook conforming to IEC/IEEE 82079-1 and ISO 20607 safety standards.
The cache stores query results, ensuring high availability and fostering user delight.
This service stands as a testament to engineering excellence in our evolving landscape.
"""
    neg_path = temp_dir / "negative_test_case.md"
    neg_path.write_text(negative_sample, encoding="utf-8")
    neg_res = doc_validator.validate_document(neg_path)
    neg_path.unlink()

    expected_forbidden = [
        "reflects the system implementation",
        "directly from the source code",
        "correspond to active production code",
        "arc42",
        "C4 Model"
    ]
    detected_all = all(any(exp in err for err in neg_res.errors) for exp in expected_forbidden)
    if detected_all and len(neg_res.errors) >= 5:
        print(f"[PASS] Guardrails successfully blocked {len(neg_res.errors)} forbidden meta-text & framework patterns.")
    else:
        print(f"[FAIL] Guardrails failed to catch all expected negative violations: {neg_res.errors}")
        all_passed = False

    # Storage Location Guideline Verification
    print("--------------------------------------------------")
    print("Running Storage Location Assertions (Checking documentation/ Directory Guideline)")
    print("--------------------------------------------------")
    root_sample_path = Path("sample_root_doc.md")
    root_sample_path.write_text("# Test Architecture\nDirect service specification.\n", encoding="utf-8")
    root_res = doc_validator.validate_document(root_sample_path)
    if root_sample_path.exists():
        root_sample_path.unlink()
    if any("documentation/" in warn for warn in root_res.warnings):
        print("[PASS] Successfully flagged root file placement with a warning to store in documentation/ folder.")
    else:
        print(f"[FAIL] Expected warning about storing in documentation/ folder, got: {root_res.warnings}")
        all_passed = False

    print("\n--------------------------------------------------")
    if all_passed:
        print("[SUCCESS] Fixed-sample structural checks passed. Operational correctness requires separate review.")
        sys.exit(0)
    else:
        print("[FAILURE] Evaluation failed. Please review errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()

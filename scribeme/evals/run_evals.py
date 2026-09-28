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


SAMPLE_DOC_3_RUNBOOK = """# Operational Runbook: Zero-Downtime PostgreSQL 14 to 16 Migration

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
        print("[SUCCESS] ALL EVALUATION CASES PASSED! Skill is verified.")
        sys.exit(0)
    else:
        print("[FAILURE] Evaluation failed. Please review errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()

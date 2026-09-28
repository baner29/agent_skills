# ADR-001: Selection of Event Streaming Platform for Order Processing

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

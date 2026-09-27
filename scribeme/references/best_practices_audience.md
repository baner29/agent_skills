# Audience Empathy, Multi-Angle Views & Docs-as-Code Best Practices

Architecture documentation fails when it becomes an impenetrable wall of technical jargon that only the original author can decipher. This reference synthesizes battle-tested industry practices from leading engineering publications (FreeCodeCamp, Substack) and editorial standards to make technical documentation immediately readable, actionable, and maintainable.

---

## 1. The 3-Angle View Framework

Different stakeholders need different information to make decisions. Rather than writing three separate documents, structure the documentation into three clear, complementary angles:

### A. Conceptual View (For PMs, UX Designers, Business Leaders)
- **Primary Focus**: What the system does for the user and business.
- **Key Concepts**: User value, business capabilities, domain workflows (e.g., "User Authentication System", "Dispute Resolution Engine").
- **Language**: Domain terminology, user impact, SLAs, compliance guarantees. Avoid internal class names or database indexing strategies.

### B. Component View (For Frontend Developers, Integration Engineers, IT Staff)
- **Primary Focus**: How the parts interact across system boundaries.
- **Key Concepts**: APIs, gateways, event buses, request payloads, response formats, sync vs. async boundaries.
- **Language**: Clean protocol descriptions (e.g., "Web App calls API Gateway $\rightarrow$ Microservice $\rightarrow$ Database").

### C. Operational View (For Backend Engineers, DevOps, SRE, Security)
- **Primary Focus**: Where the system runs, how it scales, and how it handles failure.
- **Key Concepts**: Cloud infrastructure, network topologies, database clustering, autoscaling thresholds, monitoring metrics, deployment pipelines.
- **Language**: Infrastructure specs, container resources, port bindings, failover mechanics.

---

## 2. Translating Tech into User-Relevant Outcomes

Never present raw technical specifications in isolation. Every major technical constraint, pattern, or choice should be paired with its user or business outcome using an **Outcome Translation Table**:

| Engineering Requirement | ❌ Technical Jargon (What it is) | ✅ User & Business Outcome (Why it matters) |
|---|---|---|
| **Scalability** | "Kubernetes horizontal pod autoscaling with HPA metrics" | System handles a 10x traffic surge during marketing events with zero performance degradation. |
| **Performance** | "Edge CDN caching with Redis in-memory key-value store" | Product pages load in under 300ms globally, eliminating user drop-off from slow loading screens. |
| **Security & Privacy** | "TLS 1.3 in-transit and AES-256 field-level encryption" | Customer payment details and PII are fully shielded against interception and unauthorized internal access. |
| **Data Consistency** | "Distributed transactional outbox with idempotency keys" | Users never get charged twice if they accidentally double-click "Submit Order". |
| **High Availability** | "Multi-AZ active-active database replication with failover" | Platform maintains 99.95% uptime (< 4 hours downtime per year), surviving complete cloud data center outages. |

---

## 3. Communication Clarity: Interface Dynamics

One of the largest sources of confusion in technical documentation is ambiguous service communication. Document interfaces with explicit answers to these two dimensions:

### 1. Frontend $\leftrightarrow$ Backend Interaction
- Specify exactly what protocol is used (REST, GraphQL, gRPC-Web, WebSockets).
- State what happens during loading, transient network drops, and error conditions.
- *Example*: "The React client sends a `POST /api/v1/orders` request with an `Idempotency-Key` header. If network connectivity drops before a response arrives, the client retries with the same key, guaranteeing the order is created only once."

### 2. Backend $\leftrightarrow$ Backend Interaction: Synchronous vs. Asynchronous
- Clearly categorize inter-service communication as **Synchronous** (blocking, immediate response required) or **Asynchronous** (non-blocking, message-driven, background processing).
- State expected latency and consistency models so non-backend readers understand why some operations feel instantaneous while others take several seconds:
  - *Synchronous*: "Payment authorization happens synchronously over HTTPS to Stripe (expected response time: 250–500ms). The checkout UI blocks until payment succeeds."
  - *Asynchronous*: "Order fulfillment and inventory reservation happen asynchronously via Kafka topic `order-events` (average lag: 45ms). Confirmation emails arrive in the user's inbox within 10 seconds."

---

## 4. The 13 Architecture Views Catalog

When documenting complex enterprise systems, select the appropriate subset of views from this standard taxonomy:

1. **Business Context View**: High-level business processes, user personas, partner organizations.
2. **Technical Context View**: External system integrations, network boundaries, and protocols.
3. **Logical Solution Overview**: Core subsystems and their functional responsibilities.
4. **Interface Overview**: API catalog, gRPC proto definitions, event schemas, versioning strategies.
5. **Application / Service Inventory**: List of deployable services, owners, tech stacks, and lifecycles.
6. **Data Flow View**: Pipeline from data ingestion through processing, storage, and analytics.
7. **Conceptual Data Model**: High-level entity-relationship model defining ubiquitous business terms.
8. **Logical Data Model**: Normalized data schema, key relationships, domain attributes.
9. **Physical Data Model**: Concrete database schemas, partitions, indexing strategies, cache layouts.
10. **Security View & Threat Model**: Trust boundaries, auth flows, token lifecycles, encryption schemes.
11. **Deployment View**: Cloud infrastructure topology, VPCs, subnets, Kubernetes clusters, load balancers.
12. **Runtime Sequence Diagrams**: End-to-end event sequence flows for critical user scenarios.
13. **Cloud Account / Subscription Model**: Multi-tenant cloud landing zones, IAM policies, and cost tracking.

---

## 5. Docs-as-Code Best Practices

1. **Colocate Docs in a Dedicated `documentation/` Directory**: Store all project documentation in a top-level `documentation/` directory in the active workspace path (e.g., `documentation/architecture/`, `documentation/adr/`, `documentation/runbooks/`), or in the custom path requested by the user. Never scatter loose documentation files across the repository root.
2. **Diagrams as Code Only**: Use Mermaid (` ```mermaid `) or text-based diagrams. **Avoid static PNG/JPEG screenshots of whiteboards or drawing tools**. If a service name changes, text diagrams can be updated with a simple search-and-replace, whereas static images rot immediately.
3. **Single Source of Truth**: Never duplicate descriptions across multiple documents. If a service is defined in the architecture specification, reference that document from the ADR rather than re-explaining the service.
4. **Enforce Maintainability**: *If you cannot maintain a diagram or view over time, do not create it.* Stale documentation is worse than no documentation because it introduces false assumptions into engineering decisions.

---

## 6. Human vs. AI Writing Field Guide (Wikipedia Signs of AI Writing)

Engineering documents written by humans at top technology organizations (Stripe, Netflix, Google, Datadog) sound focused, restrained, and direct. AI language models have predictable stylistic tells ([Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)). Apply the following audit table before publishing any technical document:

| AI Writing Tell | ❌ AI-Generated Pattern | ✅ Human Engineering Prose |
|---|---|---|
| **Superficial Commentary (-ing Fluff)** | "The cache stores query results, *ensuring high performance and elevating user satisfaction*." | "The cache stores query results for 300 seconds (TTL=300s)." |
| **Undue Significance & Legacy Puffs** | "This service *stands as a testament to engineering excellence, marking a pivotal moment in our evolving landscape*." | "This service authorizes payments with under 200ms P99 latency." |
| **Rule-of-Threes Adjective Stacking** | "Delivering a *robust, scalable, and resilient* architecture for microservices." | "Sustaining 10,000 req/sec across 3 GCP availability zones." |
| **Sentence-Initial Transition Spam** | "*Additionally*, the queue buffers writes. *Furthermore*, the worker drains records. *Consequently*, latency drops." | "The queue buffers incoming writes. Workers drain records in batches of 500, keeping P99 latency below 80ms." |
| **Thesaurus Inflation** | "*Utilizing* an asynchronous mechanism to *commence* synchronization." | "*Using* an asynchronous queue to *start* synchronization." |
| **Meta-Framework Quoting** | "This specification *follows the Lean arc42 framework and C4 Model Level 2 container specifications*." | "### Service Architecture & Topology" (Use the structure silently without declaring the framework name). |
| **Standards Compliance Bragging** | "Operational runbook *conforming to IEC/IEEE 82079-1 and ISO 20607 safety standards*." | "### Database Failover Runbook" (Provide the safety notices and step-by-step procedures directly). |
| **Methodology Meta-Text / Navel-Gazing** | "*This documentation suite reflects the system implementation directly from the source code. All configuration values, API contracts, database schemas, and operational parameters correspond to active production code.*" | Omit completely. State system behavior, schemas, and parameters directly without explaining how the document was compiled. |
| **Prompt Echoing / Instruction Leaking** | "*As requested, this document provides the architectural analysis based on repository inspection.*" | Omit completely. Begin directly with the document title and immediate technical overview. |


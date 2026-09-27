# Lean arc42 Architecture Documentation Framework

arc42 is an industry-standard framework for documenting and communicating software and system architectures. It provides a structured, pragmatic template containing 12 canonical sections.

In modern agile and cloud-native environments, coding agents should follow this **Lean arc42** specification to avoid unnecessary bureaucracy while maintaining total structural rigor.

> [!IMPORTANT]
> **Internal Agent Scaffolding**: This framework is for the AI agent's internal structural planning. **NEVER cite "arc42" or use section numbers (e.g. "arc42 Section 5") in the output documentation.** Real engineers at top companies do not write "arc42"; they use natural engineering headings like `System Architecture`, `Service Topology`, and `Transaction Lifecycle`.

---

## The 12 Canonical arc42 Sections

```
arc42 Architecture Blueprint
├── 1. Introduction and Goals (Requirements, Quality Goals, Stakeholders)
├── 2. Architecture Constraints (Technical, Organizational, Conventions)
├── 3. Context and Scope (Business Context & Technical Context with C4 L1)
├── 4. Solution Strategy (Fundamental decisions and architectural style)
├── 5. Building Block View (Decomposition Level 1 & Level 2 with C4 L2/L3)
├── 6. Runtime View (Key scenarios & Sequence Diagrams)
├── 7. Deployment View (Infrastructure, Cloud topology, Environments)
├── 8. Crosscutting Concepts (Security, Observability, Persistence, Error Handling)
├── 9. Architecture Decisions (ADR references & summary log)
├── 10. Quality Requirements (Quality tree and concrete quality scenarios)
├── 11. Risks and Technical Debt (Identified risks & mitigation plans)
└── 12. Glossary (Ubiquitous language and acronyms)
```

---

## Section-by-Section Authoring Guide

### 1. Introduction and Goals
- **Requirements Overview**: 2–3 paragraphs describing the core problem, user value proposition, and key features.
- **Top 3 Quality Goals**: High-priority architectural non-functional requirements (e.g., Availability 99.95%, P99 Latency < 100ms, Horizontal Scalability).
- **Stakeholder Matrix**:
  | Role / Stakeholder | Goal / Interest in System | Expectations from Architecture |
  |---|---|---|
  | Product Manager | High conversion rate, fast time-to-market | Extensible feature modularity |
  | Security Officer | Zero unauthorized PII exposure | TLS 1.3, RBAC, encrypted storage at rest |
  | SRE / DevOps | High availability, low pager alert noise | Health checks, metrics, fast restart |

### 2. Architecture Constraints
Document hard constraints that cannot be negotiated:
- **Technical Constraints**: Target cloud platform (e.g., GCP Cloud Run / GKE), programming languages, required database engines.
- **Organizational Constraints**: Team size, budget ceilings, delivery timelines, regulatory compliance (e.g., HIPAA, GDPR, PCI-DSS).
- **Conventions**: Git workflow, semantic versioning, OpenAPI documentation standards.

### 3. Context and Scope
Clearly delineate the system boundary from external entities:
- **Business Context**: Non-technical explanation of who interacts with the system (users, partner organizations).
- **Technical Context**: Protocols, data formats, and physical network boundaries.
- **Diagram**: Must include a **C4 Level 1 System Context Diagram** in Mermaid format.

### 4. Solution Strategy
Summarize the foundational architectural decisions:
- Architectural paradigm: Microservices vs. Modular Monolith vs. Event-Driven.
- Data storage strategy: Polyglot persistence, relational vs. document/key-value.
- Integration patterns: Asynchronous event streaming vs. synchronous REST/gRPC.

### 5. Building Block View
Hierarchical decomposition of the software system:
- **Level 1 (System Containers)**: High-level deployable units (Web App, API Gateway, Microservices, Databases). Include a **C4 Level 2 Container Diagram**.
- **Level 2 (Internal Components)**: Internal structure of the most critical containers. Include a **C4 Level 3 Component Diagram**.

### 6. Runtime View
Describe the dynamic behavior of the system across critical runtime scenarios:
- **Happy Path Flow**: End-to-end user transaction flow.
- **Failure / Compensation Flow**: Handling network timeouts, payment declines, or queue dead-letter routing.
- **Diagram**: Must include a **Mermaid Sequence Diagram** with step-by-step numbered lifelines.

### 7. Deployment View
Map software building blocks onto physical or cloud infrastructure:
- Cloud infrastructure topology (VPC, subnets, Kubernetes clusters, Serverless runtimes).
- Configuration per environment (Local Development, Staging, Production).
- Scaling and redundancy topology (Multi-region, autoscaling parameters, replicas).

### 8. Crosscutting Concepts
Document patterns applied uniformly across components:
- **Security & Identity**: Authentication (OAuth2/OIDC), authorization (RBAC/ABAC), secret management, data encryption.
- **Observability**: Metrics (Prometheus), structured logging (JSON correlation IDs), distributed tracing (OpenTelemetry).
- **Resilience & Fault Tolerance**: Circuit breakers, exponential backoff retries, rate limiting, dead-letter queues.
- **Data Consistency & Transactions**: Outbox pattern, idempotency keys, CQRS.

### 9. Architecture Decisions
Index of key decisions made during the system design. Every major decision links to an ADR:
| ADR ID | Decision Title | Status | Date |
|---|---|---|---|
| [ADR-001](file:///docs/adr/001-kafka-streaming.md) | Asynchronous Event Streaming with Kafka | Accepted | 2026-02-15 |
| [ADR-002](file:///docs/adr/002-postgresql-storage.md) | Relational Storage for Order Ledgers | Accepted | 2026-02-18 |

### 10. Quality Requirements
Structure quality requirements into a **Quality Tree** with verifiable scenarios:
- **Format**: `[Quality Category] -> [Aspect] -> [Concrete Scenario]`
- **Example Scenario**:
  - *Stimulus*: 10,000 concurrent users checkout within 60 seconds during a flash sale.
  - *Response*: System autoscales from 4 to 20 instances; P99 response time remains under 250ms with 0% dropped transactions.

### 11. Risks and Technical Debt
Table of known architectural risks, their severity, and planned mitigations:
| Risk / Technical Debt Item | Likelihood | Impact | Planned Mitigation Strategy |
|---|---|---|---|
| Single third-party payment provider dependency | Low | Critical | Implement secondary fallback gateway adapter (Stripe + Adyen) |
| Monolithic database connection pool exhaustion | Medium | High | Introduce PgBouncer connection pooling layer |

### 12. Glossary
Alphabetical table defining domain-specific terminology, business entities, and technical acronyms to ensure a shared ubiquitous language between business and engineering stakeholders.

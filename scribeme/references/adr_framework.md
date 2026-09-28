# Architecture Decision Record (ADR) Framework

Architecture Decision Records (ADRs) capture significant architectural decisions along with their context, rationale, and consequences. They ensure that technical decisions are transparent, searchable, and maintainable over time.

> [!IMPORTANT]
> **Internal Agent Scaffolding**: MADR and the Y-statement formula are the AI agent's internal reasoning tools. **NEVER cite "MADR" or label headings as "Executive Y-Statement" in output documentation.** Embed the 5-clause reasoning naturally under `## Decision Outcome` or `### Decision Summary`.

---

## 1. When to Write an ADR

Write an ADR whenever a technical decision meets any of the following criteria:
- **High Blast Radius**: Affects multiple services, teams, or external consumers.
- **Irreversibility / High Switching Cost**: Database selection, communication protocols (REST vs. gRPC vs. GraphQL), framework or language migrations.
- **Trade-off Resolution**: Choosing between competing quality attributes (e.g., strong consistency vs. low latency, operational complexity vs. flexibility).
- **Standards & Conventions**: Adopting an organizational pattern (e.g., event-driven choreography vs. orchestrator).

---

## 2. Decision Status Lifecycle

Every ADR must declare its current lifecycle status:

```
[ Proposed ] ──────► [ Accepted ] ──────► [ Deprecated ]
       │                     │
       ▼                     ▼
  [ Rejected ]          [ Superseded (by ADR-XXX) ]
```

- **Proposed**: Under review and RFC discussion.
- **Accepted**: Approved and active engineering policy.
- **Rejected**: Evaluated and discarded (documents *why* we didn't pursue an idea).
- **Deprecated**: Previously accepted, but no longer recommended for new systems.
- **Superseded**: Replaced by a newer decision (must reference the successor ADR).

---

## 3. The Y-Statement Formula

Every ADR executive summary MUST include an explicit **Y-Statement** following this standard syntax:

```text
In the context of {system context / business situation},
facing {technical challenge / non-functional requirement},
we decided for {chosen architecture option},
to achieve {key positive outcome / quality attribute},
accepting {known trade-off / negative consequence}.
```

### Example Y-Statement:
> "In the context of the high-throughput order processing service,
> facing peak flash-sale loads exceeding 50,000 transactions per second,
> we decided for an asynchronous event-driven architecture using Apache Kafka,
> to achieve decoupled service resilience and sub-second ingestion latency,
> accepting eventual consistency across downstream analytics services and higher operational cluster complexity."

---

## 4. Standard ADR Markdown Template (MADR 3.0 Standard)

Use this complete template when authoring an ADR:

```markdown
# ADR-001: [Short Title of the Decision]

- **Status**: [Proposed | Accepted | Rejected | Deprecated | Superseded by ADR-XXX]
- **Date**: YYYY-MM-DD
- **Deciders**: [List authors, tech leads, architects]
- **Technical Story**: [Link to Jira / GitHub Issue / RFC]

## Context and Problem Statement
[Describe the context and the problem being solved in 1–2 paragraphs. Explain what changed, what constraints exist, and why a decision is necessary right now.]

## Decision Drivers (Forces)
- [Driver 1: e.g., Must support 100k active concurrent WebSocket sessions]
- [Driver 2: e.g., P99 API response time must remain under 200ms]
- [Driver 3: e.g., Must comply with GDPR data isolation mandates]
- [Driver 4: e.g., Team operational familiarity and cloud cost limits]

## Considered Options
1. **Option A**: [Name of Option A]
2. **Option B**: [Name of Option B]
3. **Option C**: [Name of Option C]

## Decision Outcome
Chosen option: **Option A**, because [succinct justification].

### Decision Summary
> In the context of [context],
> facing [problem/driver],
> we decided for [Option A],
> to achieve [benefit],
> accepting [trade-off].

---

## Pros and Cons of the Options

### Option A: [Chosen Option]
- **Good**, because [positive consequence 1]
- **Good**, because [positive consequence 2]
- **Bad**, because [negative trade-off 1]
- **Bad**, because [operational risk or complexity]

### Option B: [Rejected Alternative]
- **Good**, because [positive aspect]
- **Bad**, because [rejection reason, e.g., failed latency benchmark]

### Option C: [Rejected Alternative]
- **Good**, because [positive aspect]
- **Bad**, because [rejection reason, e.g., licensing cost or vendor lock-in]

---

## Trade-off Analysis Matrix

| Evaluation Criteria | Option A (Chosen) | Option B | Option C |
|---|---|---|---|
| **P99 Latency (<200ms)** | ✅ 45ms | ⚠️ 180ms | ❌ 410ms |
| **Operational Overhead** | ⚠️ Moderate (managed cloud) | ✅ Low (serverless) | ❌ High (self-hosted) |
| **Data Consistency** | Eventual (50ms lag) | Strong | Strong |
| **Estimated Monthly Cost** | $1,200 | $3,400 | $800 |
| **Team Skillset Match** | High | High | Low |

---

## Consequences & Mitigation

### Positive Consequences
- [Positive consequence 1]
- [Positive consequence 2]

### Negative Consequences & Mitigations
- **Trade-off**: Eventual consistency means UI might display stale inventory counts for up to 100ms.
  - *Mitigation*: Optimistic UI updates with client-side reconciliation.
- **Trade-off**: Additional infrastructure component to monitor.
  - *Mitigation*: Enable Datadog Kafka integration with alert on consumer group lag > 10,000 messages.

---

## Validation & Verification Plan
- [ ] Load test deployed prototype under 1.5x peak volume.
- [ ] Verify Prometheus metric alerts fire when dead-letter queue receives messages.
- [ ] Schedule architectural review 6 months post-launch to evaluate operational burden.
```

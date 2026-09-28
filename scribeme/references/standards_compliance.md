# Standards Compliance Reference: Technical Documentation & Plain Language

This guide operationalizes the four mandatory global standards governing technical documentation, software engineering artifacts, user instruction manuals, and plain language communication.

> [!IMPORTANT]
> **Internal Agent Scaffolding**: This reference is for the AI agent's internal authoring process. **NEVER cite or mention "IEC/IEEE 82079-1", "ISO 20607", "ISO/IEC/IEEE 15289", or "ISO 24495-1" in human-facing documentation.** Apply the principles silently to structure procedures, alert boxes, and plain prose without declaring standard compliance.

---

## 1. IEC/IEEE 82079-1: Preparation of Information for Use (User Manuals & Technical Instructions)

IEC/IEEE 82079-1 establishes global requirements for creating clear, usable, and reliable documentation for systems, products, and software.

### Core Principles
1. **Audience-Centric Task Orientation**: Structure information around user tasks rather than internal implementation mechanics.
2. **Minimalism**: Provide all necessary information, but eliminate extraneous filler that distracts the reader from completing the task.
3. **Information Typing (DITA Concept)**: Strictly categorize every section into one of three information types:
   - **Concept**: Explains *what* something is and *why* it works (conceptual mental model, architecture context).
   - **Task**: Explains *how* to do something with ordered, numbered, imperative steps (e.g., deployment, installation, configuration).
   - **Reference**: Factual lookup data (API tables, environment variables, CLI parameter flags, error codes). Do not bury procedural steps inside reference tables.
4. **Scannability & Information Architecture**:
   - Limit paragraphs to 3–4 sentences.
   - Use descriptive, action-oriented headings (e.g., `Deploying to Production Cluster` instead of `Cluster Information`).
   - Use tables for comparative or tabular data.
   - Use bold keywords for UI elements, flags, and parameter names.

### Procedural Task Rules (IEC/IEEE 82079-1 Task Schema)
Every procedural section MUST follow this four-part structure:
```markdown
### [Action Verb] [Task Objective]

**Prerequisites**:
- [List required credentials, tools, permissions, and initial state]

**Procedure**:
1. Execute command or action in active imperative voice:
   ```bash
   run action --flag
   ```
2. Verify intermediate output:
   > Expected output: `Status: READY`
3. Perform the next consecutive action.

**Verification**:
Confirm that [expected end-state is reached, e.g., service responds at `https://localhost:8080/health` with HTTP 200].

---

## 2. ISO 20607: Safety of Technical Systems & Instruction Handbooks

ISO 20607 governs safety instructions, operational risk reduction, and hazard callouts in technical and machinery systems. When documenting systems that involve data loss, downtime, security vulnerabilities, or operational hazards, use the standard ISO 20607 safety signal hierarchy.

### Safety Alert Hierarchy
Never use casual bold text or ad-hoc emojis for critical warnings. Use standard GitHub/Markdown alert boxes mapped to ISO 20607 hazard levels:

| Signal Word | Markdown Syntax | Risk Level & Definition | Required Content |
|---|---|---|---|
| **DANGER** | `> [!CAUTION]` with **DANGER** header | **Immediate High Risk**: Will result in catastrophic system failure, irreversible data loss, or severe security breach. | Nature of hazard, immediate consequence, exact avoiding action. |
| **WARNING** | `> [!WARNING]` | **Moderate/Substantial Risk**: Could result in extended service downtime, data corruption, or credential exposure. | Source of risk, threshold conditions, corrective action. |
| **CAUTION** | `> [!CAUTION]` | **Minor/Moderate Risk**: Could cause performance degradation, unexpected cache invalidation, or non-fatal configuration drift. | Operational hazard, potential impact, preventative measure. |
| **NOTICE** | `> [!NOTE]` or `> [!IMPORTANT]` | **Operational Risk / Property**: System behavior notice, license constraint, or dependency prerequisite. Non-injury/non-catastrophic. | Best practice, policy constraint, or maintenance tip. |

### Safety Notice Construction Template
Every hazard notice must contain:
1. **Signal Word & Type of Hazard**
2. **Consequence of Non-Compliance**
3. **Exact Preventative or Corrective Action**

```markdown
> [!WARNING]
> **Data Loss Risk**: Executing `DROP TABLE staging_orders` without taking a manual snapshot will permanently delete uncommitted transactions from the last 2 hours.
> **Required Action**: Execute `pg_dump -t staging_orders dbname > backup.sql` before running this migration script.
```

---

## 3. ISO/IEC/IEEE 15289: Life-Cycle Information Items (System & Software Documentation)

ISO/IEC/IEEE 15289 standardizes the identification and content requirements for software and systems life-cycle documents.

### Primary Life-Cycle Information Items & Required Content
When generating software documentation, map the document to its standard IEEE 15289 information item:

#### 1. System Architecture Description (SAD)
- **Scope & Context**: System purpose, business goals, and boundary with external entities.
- **Architectural Views**: Functional/logical view, physical/deployment view, process/runtime view, data view.
- **Design Rationale**: Architectural decisions, rejected alternatives, and trade-off justification.
- **Traceability**: Mapping from architectural components to functional requirements.

#### 2. Software Design Description (SDD)
- **Component Decomposition**: Identification of sub-systems, services, modules, and interfaces.
- **Interface Definitions**: Data contracts, protocol specifications (HTTP/gRPC/AMQP), request/response schemas, error handling.
- **Data Models**: Entity relationships, storage schemes, and persistence layer design.
- **Dynamic Behavior**: State machine transitions, event sequences, and concurrency controls.

#### 3. Verification & Validation Plan / Test Specification
- **Test Strategy**: Unit, integration, end-to-end, load, and security test scopes.
- **Acceptance Criteria**: Quantifiable performance metrics (latency, throughput, MTTR).
- **Environment Prerequisites**: Staging specifications, mock services, test datasets.

---

## 4. ISO 24495-1: Plain Language Governing Principles

ISO 24495-1 defines plain language as communication where wording, structure, and design are so clear that the intended readers can:
1. **Find** what they need,
2. **Understand** what they find, and
3. **Use** what they find to meet their needs.

### Operational Plain Language Rules for Coding Agents

#### Rule 1: Use Active Voice with Concrete Technical Actors
- ❌ *Passive / Anonymous*: "The payment payload is validated by the system and then an order confirmation event is dispatched."
- ✅ *Active / Concrete*: "The `CheckoutService` validates the payment payload and publishes an `OrderConfirmed` event to the `orders-topic`."

#### Rule 2: Eliminate AI Boosterism and Generic Residue
Remove empty intensifiers that provide zero engineering information:
- ❌ "This cutting-edge service plays a pivotal role in ensuring seamless, robust, and highly scalable user experiences across the entire landscape."
- ✅ "The `AuthService` issues signed JWT tokens and validates session cookies within 15 milliseconds."

#### Rule 3: Unpack Nominalizations into Clear Verbs
Nominalizations (turning verbs into clumsy abstract nouns) obscure technical causality:
- ❌ "Execution of the synchronization of databases is performed through the utilization of an asynchronous queue."
- ✅ "The worker process synchronizes the two databases asynchronously using a Redis queue."

#### Rule 4: Match Vocabulary to Reader Persona
- For **Business/Product Stakeholders**: Express features in terms of business capability, SLA, cost, and user outcome.
- For **Developers/Engineers**: Express features in terms of code modules, API endpoints, serialization formats, and thread safety.
- For **Operations/SRE**: Express features in terms of resource consumption, port bindings, metric endpoints, health checks, and restart policies.

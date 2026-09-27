# C4 Model Diagramming Reference (Mermaid Diagrams-as-Code)

The C4 model (Context, Containers, Components, and Code) provides a hierarchical way to describe software architecture using different levels of zoom.

All diagrams generated under this skill MUST be written in pure **Mermaid markdown** (` ```mermaid `) so they render natively in GitHub, GitLab, Notion, and Markdown viewers without external binary dependencies.

> [!IMPORTANT]
> **Internal Agent Scaffolding**: C4 levels are the AI agent's mental model for zoom abstraction. **NEVER label headings as "C4 Model Level 1 System Context" or "C4 Level 2 Container Diagram" in generated documentation.** Instead, use natural headings like `### System Context`, `### Service Architecture`, and `### Component Interactions`.

---

## 1. The 4 Levels of Abstraction

| Level | Diagram Name | Audience | Answers | Key Elements |
|---|---|---|---|---|
| **Level 1** | **System Context** | Everyone (PM, UX, Devs, Ops, Execs) | *What is the software system and who uses it?* | System boundary, human users/personas, external third-party software systems. |
| **Level 2** | **Container** | Developers, DevOps, SRE, Architects | *What is the high-level technical shape of the system?* | Deployable units: web apps, single-page apps, mobile apps, API backends, databases, message buses, file stores. |
| **Level 3** | **Component** | Developers, Software Engineers | *How are the containers structured internally?* | Services, controllers, repositories, workers, queues within a single container. |
| **Level 4** | **Code** | Developers (Optional / Rarely Documented) | *How are classes/interfaces implemented?* | Class diagrams, ER diagrams. (Document only for complex domain patterns). |

---

## 2. Diagram Rules & Formatting Conventions

1. **Explicit Naming**: Every node must show **Name**, **[Technology / Type]**, and a brief **1-sentence description** of its role.
2. **Labeled Arrows**: Every relationship arrow must have an action verb and specify the protocol or communication mechanism (e.g., `HTTPS / JSON`, `gRPC`, `AMQP / Kafka`).
3. **Clear Boundaries**: Use Mermaid `subgraph` blocks to visually demarcate system boundaries and external scopes.
4. **Directionality**: Default to top-down (`flowchart TD`) or left-to-right (`flowchart LR`) flows. Keep the main user flow legible.

---

## 3. Copy-Pasteable Mermaid Templates

### Level 1: System Context Diagram Template

```mermaid
flowchart TD
    classDef person fill:#08427B,stroke:#073B6F,color:#ffffff,stroke-width:2px;
    classDef internalSystem fill:#1168BD,stroke:#0B4884,color:#ffffff,stroke-width:2px;
    classDef externalSystem fill:#999999,stroke:#666666,color:#ffffff,stroke-width:2px;

    User["👤 Customer<br/>[Person]<br/>Browses products, places orders, and manages account"]:::person
    Staff["👤 Support Agent<br/>[Person]<br/>Reviews customer orders and resolves disputes"]:::person

    subgraph Boundary["Enterprise System Boundary"]
        System["📦 E-Commerce Platform<br/>[Software System]<br/>Handles product catalog, cart checkout, and inventory tracking"]:::internalSystem
    end

    PaymentGateway["🏢 Stripe API<br/>[External System]<br/>Processes credit card payments and refunds"]:::externalSystem
    EmailService["🏢 SendGrid API<br/>[External System]<br/>Sends transactional emails and alerts"]:::externalSystem

    User -->|"Browses items and purchases<br/>[HTTPS]"| System
    Staff -->|"Manages dispute cases<br/>[HTTPS / Admin Portal]"| System
    System -->|"Authorizes charges and captures funds<br/>[HTTPS / REST]"| PaymentGateway
    System -->|"Dispatches order confirmations<br/>[HTTPS / Webhook]"| EmailService
```

---

### Level 2: Container Diagram Template

```mermaid
flowchart TD
    classDef user fill:#08427B,stroke:#073B6F,color:#ffffff,stroke-width:2px;
    classDef webApp fill:#2B78C5,stroke:#1B4F82,color:#ffffff,stroke-width:2px;
    classDef api fill:#1168BD,stroke:#0B4884,color:#ffffff,stroke-width:2px;
    classDef database fill:#255B98,stroke:#173B63,color:#ffffff,stroke-width:2px;
    classDef external fill:#999999,stroke:#666666,color:#ffffff,stroke-width:2px;

    Customer["👤 Customer<br/>[Person]"]:::user

    subgraph SystemBoundary["E-Commerce System"]
        SPA["🌐 Single-Page Application<br/>[Container: React / TypeScript]<br/>Provides user interface in browser"]:::webApp
        API["⚙️ API Gateway & Backend<br/>[Container: Go / Gin]<br/>Exposes REST endpoints and business logic"]:::api
        OrderDB[("🗄️ Order Database<br/>[Container: PostgreSQL]<br/>Stores order records and customer transactions")]:::database
        Cache[("⚡ Session Cache<br/>[Container: Redis]<br/>Caches user sessions and shopping carts")]:::database
        Queue["📨 Event Broker<br/>[Container: Apache Kafka]<br/>Publishes asynchronous domain events"]:::api
    end

    PaymentService["🏢 Stripe API<br/>[External System]"]:::external

    Customer -->|"Interacts with UI<br/>[HTTPS]"| SPA
    SPA -->|"Fetches data & submits orders<br/>[JSON / HTTPS]"| API
    API -->|"Reads/writes cart state<br/>[TCP / RESP]"| Cache
    API -->|"Reads & writes order records<br/>[TCP / Port 5432]"| OrderDB
    API -->|"Publishes OrderPlaced events<br/>[TCP / Port 9092]"| Queue
    API -->|"Captures payment charges<br/>[HTTPS / REST]"| PaymentService
```

---

### Level 3: Component Diagram Template

```mermaid
flowchart TD
    classDef component fill:#438DD5,stroke:#2E6295,color:#ffffff,stroke-width:2px;
    classDef external fill:#255B98,stroke:#173B63,color:#ffffff,stroke-width:2px;

    Client["🌐 Web SPA / Mobile App<br/>[External Caller]"]

    subgraph BackendContainer["API Backend Container [Go]"]
        OrderController["🎮 OrderController<br/>[Component: Gin Handler]<br/>Validates incoming HTTP order payloads"]:::component
        OrderService["💼 OrderService<br/>[Component: Domain Service]<br/>Coordinates business logic and payment calls"]:::component
        PaymentClient["🔌 PaymentClient<br/>[Component: HTTP Adapter]<br/>Encapsulates communication with Stripe API"]:::component
        OrderRepo["💾 OrderRepository<br/>[Component: GORM / SQL]<br/>Persists order entities to PostgreSQL"]:::component
        EventProducer["📢 EventProducer<br/>[Component: Kafka Producer]<br/>Serializes and emits domain events"]:::component
    end

    PostgresDB[("🗄️ Orders DB [PostgreSQL]")]:::external
    KafkaCluster["📨 Kafka Topic [orders-v1]"]:::external
    StripeAPI["🏢 Stripe REST API"]:::external

    Client -->|"POST /api/v1/orders<br/>[JSON / HTTPS]"| OrderController
    OrderController -->|"Parses & calls PlaceOrder()"| OrderService
    OrderService -->|"Executes charge"| PaymentClient
    PaymentClient -->|"POST /v1/charges"| StripeAPI
    OrderService -->|"Saves completed order"| OrderRepo
    OrderRepo -->|"INSERT INTO orders"| PostgresDB
    OrderService -->|"Emits OrderPlaced event"| EventProducer
    EventProducer -->|"Publishes to topic"| KafkaCluster
```

---

## 4. Sequence Diagram Template (Runtime View)

```mermaid
sequenceDiagram
    autonumber
    actor Customer as 👤 Customer
    participant UI as 🌐 Web App (SPA)
    participant API as ⚙️ API Backend
    participant DB as 🗄️ PostgreSQL
    participant Pay as 🏢 Stripe Gateway
    participant Bus as 📨 Kafka

    Customer->>UI: Clicks "Complete Purchase"
    UI->>API: POST /api/v1/orders (CartID, PaymentToken)
    activate API
    API->>API: Validate payload & idempotency key
    API->>Pay: Authorize & capture charge ($99.00)
    activate Pay
    Pay-->>API: 200 OK (ChargeID: ch_12345)
    deactivate Pay
    API->>DB: BEGIN TRANSACTION; INSERT order; COMMIT;
    activate DB
    DB-->>API: Row written (OrderID: ord_987)
    deactivate DB
    API->>Bus: Publish event `OrderPlaced(ord_987)`
    API-->>UI: 201 Created (OrderID: ord_987, Status: CONFIRMED)
    deactivate API
    UI-->>Customer: Renders confirmation screen
```

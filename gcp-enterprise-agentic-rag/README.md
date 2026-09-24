# GCP Enterprise Agentic RAG Skill

> Standardized, serverless multi-agent RAG framework on Google Cloud Platform.

This skill makes your coding agents build, configure, validate, and deploy an enterprise-grade multi-agent system on Vertex AI Agent Runtime with automated memory bank persistence, Cloud DLP privacy redaction, BigQuery ML, and Vertex AI Search.

![1790213650772](image/README/1790213650772.jpg)

Goal
----

Deploying a production grade agentic application requires lot of work, including - choosing the right set of tools - orchestrator, model, short-term memory (sessions), long-term memory, PII masking, logging and monitoring, security, agent-tools, policies, search engine (RAG), and evaluation. After deciding the tools, the next big challenge is how to connect these tools together (designing the architecture). The final headache is where to deploy and ensure your agents are accessible to your team mates and others who you want to access these agents.

This skill does this heavy lifting for you. It is designed after learning from mutliple production grade agentic architectures which are used by various teams within an enterprise.

The goal is simple, developing and deploying an agent should be the least effort task. The focus should be on the core logic of your agents.

How it works?
-------------

This skill encapsulates the work into 8 different steps. Each step performs key operation that results deployment of a major aspect of the agent. Let's look at each of these steps briefly:

1. **Ask questions:** First step of this skill is to ask the user fundamental clarifying questions like name of the application, gcp-project-id, region of deployment, number of sub-agents and their job, etc.
2. **Pre-requisite setup:** Then it executes few pre-requisite actions like enabling GCP APIs, granting permissions, adding agent skills, plugins, and mcp-servers.
3. **Writing the code:** Then it writes the boilerplate code for ADK orchestration, Vertex AI runtime engine, and DLP functions.
4. **Pre-deployment validation:** Runs automated validations to test the foundational code.
5. **RAG & DLP setup:** It then executes setup queries for deploying RAG and DLP pipelines.
6. **Vertex AI Agent Runtime setup:** It then deploys the agent runtime on vertex AI.
7. **Post-deployment validations:** It executes post-deployment validation queries to test the working of the agent on the agent runtime.
8. **Generate documentation:** Finally, it generates a comprehensive README.md file capturing the detailed working of the agent, how to use it on the Agent Runtime, and how to test it using the Playground on the GCP console.

## Installation via `skills.sh` / `npx`

This skill is compatible with the [skills.sh](https://skills.sh) registry and can be installed into any workspace using the Skills CLI:

### 1. Install from GitHub Repository

```bash
npx skills add https://github.com/baner29/agent_skills --skill gcp-enterprise-agentic-rag
```

### 2. Install from Tree URL

```bash
npx skills add https://github.com/baner29/agent_skills/tree/main/.agents/skills/gcp-enterprise-agentic-rag
```

### 3. Install for Specific Agents

```bash
# Install to Claude Code and Cursor
npx skills add https://github.com/baner29/agent_skills --skill gcp-enterprise-agentic-rag --agent claude-code cursor

# Install globally across all projects
npx skills add https://github.com/baner29/agent_skills --skill gcp-enterprise-agentic-rag -g
```

---

## Directory Structure

Conforming to the Agent Skills standard with progressive disclosure:

```text
gcp-enterprise-agentic-rag/
├── SKILL.md                 # Core instructions, checklist & pointers (<150 lines)
├── README.md                # Skill overview, design diagrams & npx installation instructions
├── references/              # On-demand technical documentation (loaded when needed)
│   ├── discovery.md         # Phase 1: Requirements interview questionnaire
│   ├── prerequisites.md     # Phase 2: GCP APIs, IAM least-privilege roles, MCP tools
│   ├── architecture.md      # Phase 3: Code layout, ADK state builders, root_agent wiring
│   ├── rag_pipeline.md      # Phase 5: Pub/Sub, Cloud DLP, BigQuery ML remote model, Discovery Engine
│   ├── agent_runtime.md     # Phase 6: Vertex AI Agent Engine setup, AdkApp deployment
│   ├── gotchas.md           # Critical edge cases, workarounds, and telemetry flags
│   └── documentation.md     # Phase 8: Application documentation & GCP Playground testing guide
├── scripts/                 # Self-contained validation and automation scripts
│   ├── check_prereqs.sh     # Infrastructure pre-requisites verification
│   ├── setup_bq_ml.sh       # BigQuery ML & Cloud Resource Connection automated setup
│   ├── validate_agent.py    # Pre-deployment codebase self-validation loop
│   └── verify_deployment.py # Post-deployment live GCP self-validation
└── assets/                  # Starter code templates
    ├── template_agent.py    # Orchestrator & sub-agent starter template
    ├── template_deploy.py   # Agent Runtime deployment template
    └── template_cf_main.py  # Cloud Function Gen 2 with Cloud DLP sanitization
```

---

## Specification Validation

Verify that this skill conforms to the Agent Skills specification:

```bash
npx skills-ref validate .
npx skills-ref read-properties .
```

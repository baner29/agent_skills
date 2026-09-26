# 🧠 Agent Skills 

A curated collection of production agent skills for AI coding agents (Claude Code, Cursor, Codex, OpenClaw, Antigravity, GitHub Copilot, and any other agent compatible with [`skills-md`](https://agentskills.io/home)). Each skill provides specialized architecture blueprints, automated self-validation scripts, templates, and pre-deployment checklists.

---

## Skills

| Skill | Description | Installation |
| :--- | :--- | :--- |
| 🤖 [`gcp-enterprise-agentic-rag`](./gcp-enterprise-agentic-rag/) | Scaffold, configure, self-validate, and deploy serverless multi-agent systems on Google Cloud Platform with ADK, Vertex AI Agent Runtime, persistent memory banks, Cloud DLP PII sanitization, BigQuery ML summarization, and Vertex AI Search. | `npx skills add baner29/agent_skills --skill gcp-enterprise-agentic-rag` |

There are many agents skills being developed and released at a rapid scale by community contributors. Our aim is to ensure the skills we release solve production grade problems. Stay tuned for more exicting releases soon.

---

## Installation & Discovery

This repository is compatible with the [Agent Skills Standard](https://skills.sh) (`npx skills add`) and includes a machine-readable [registry.json](./registry.json) catalog.

### Option 1: Install with `npx skills` (Recommended)

Browse available skills before installing:
```bash
npx skills add baner29/agent_skills --list
```

Install a specific skill:
```bash
npx skills add baner29/agent_skills --skill gcp-enterprise-agentic-rag
```

Install all skills in the repository:
```bash
npx skills add baner29/agent_skills
```

Install globally across all projects:
```bash
npx skills add baner29/agent_skills -g
```

### Option 2: Manual Setup

Copy the target skill directory directly into your agent's skills configuration folder:

| Agent | Skills dir | 
| :--- | :--- |
| **Antigravity CLI** | `.agents/skills/<skill-name>` |
| **Gemini CLI** |`~/.gemini/config/skills/<skill-name>` |
| **Claude Code** |`./claude/skills/<skill-name>` |
| **Cursor** | `.agents/skills/<skill-name>` |
| **Github Copilot/ VS Code** |`~/.copilot/skills/<skill-name>` |
| **Codex** |`~/.cursor/skills/<skill-name>` |
| **OpenClaw** |`~/.openclaw/skills/<skill-name>` |

To make the skills globally available for all your coding agents, put the skill in `~/.agents/skills/` and execute `ln -s ~/.agents/skills/<skill-name> ~/.gemini/config/skills/<skill-name>` (MAC) and `mklink /D "%USERPROFILE%\.gemini\config\skills\<skill-name>" "%USERPROFILE%\.agents\skills\<skill-name>"` (Windows) for each agent.

---

## Use the installed skill

Open your target project in the coding agent and ask for a task either by calling the skill or without it. The skills are equipped with trigger phrases (see `evals/triggers/` for examples) that will invoke the skill. For example:

```text
Plan a customer-support agent on
Google Cloud with persistent memory and sensitive-data redaction.
Start by gathering requirements and checking prerequisites.
```

The skill’s workflow starts with requirements discovery, followed by prerequisite checks, scaffolding, validation, and deployment. The example requests the planning stages; the [skill instructions](./<skill-name>/SKILL.md) describe the complete workflow.

If your agent doesn’t discover the skill, check that the installer targeted the correct agent and project or user scope. For manual installations, confirm that `SKILL.md` sits directly inside the skill directory and that supporting files remain alongside it.

## Repository Architecture

```text
agent_skills/
├── registry.json                 # Skill catalog and metadata
├── README.md                     # Catalog and installation instructions
├── gcp-enterprise-agentic-rag/
│   ├── SKILL.md                  # Agent instructions and metadata
│   ├── README.md                 # Setup and architecture guide
│   ├── references/               # Service details and known issues
│   ├── scripts/                  # Setup and validation scripts
│   └── assets/                   # Code templates
└── evals/
    ├── triggers/                 # Queries that should or shouldn’t match
    ├── quality/                  # Test prompts and assertions
    ├── fixtures/                 # Test data
    ├── grade_evals.py            # Assertion grader
    └── run_evals.py              # Evaluation runner
```

---

## Evaluation & Benchmarking

The repository includes an automated evaluation harness adhering to the [Agent Skills Evaluation Specification](https://agentskills.io/skill-creation/evaluating-skills).

### Running Evaluations

Run the complete evaluation suite (trigger accuracy + output quality benchmarks):
```bash
python3 evals/run_evals.py --skill <skill-name>
```

Run only trigger accuracy tests:
```bash
python3 evals/run_evals.py --skill <skill-name> --mode triggers
```

Run only quality assertion benchmarks:
```bash
python3 evals/run_evals.py --skill <skill-name> --mode quality
```

### Benchmark Metrics

Evaluation results and assertion grading artifacts are written to `evals/workspace/iteration-N/`:
- `grading.json`: Granular AST, code, and script assertion results with concrete evidence.
- `timing.json`: Duration and simulated token usage.
- `benchmark.json`: Pass-rate comparison comparing with-skill execution against unguided baseline.

## Contribute a skill

See the [contribution guide](./contributing.md) for package requirements, evaluation cases, and validation steps.

## License

This repository uses the [Apache License 2.0](./LICENSE).

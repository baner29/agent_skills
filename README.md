# Agent Skills 

A curated collection of production agent skills for AI coding agents (Claude Code, Antigravity, Cursor, GitHub Copilot, Codex, and ADK-based agents). Each skill provides specialized architecture blueprints, automated self-validation scripts, templates, and pre-deployment checklists.

---

## Available Skills

| Skill | Description | Category | Installation |
| :--- | :--- | :--- | :--- |
| [`gcp-enterprise-agentic-rag`](./gcp-enterprise-agentic-rag/) | Scaffold, configure, self-validate, and deploy serverless multi-agent systems on Google Cloud Platform with ADK, Vertex AI Agent Runtime, persistent memory banks, Cloud DLP PII sanitization, BigQuery ML summarization, and Vertex AI Search. | Cloud Infrastructure | `npx skills add baner29/agent_skills --skill gcp-enterprise-agentic-rag` |

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

### Option 2: Manual / Custom Agent Setup

Copy the target skill directory directly into your agent's skills configuration folder:

- **Antigravity / Gemini CLI**: `~/.gemini/config/skills/<skill-name>`
- **Claude Code**: `.claude/skills/<skill-name>`
- **Cursor / VS Code**: `.agents/skills/<skill-name>`

---

## Repository Architecture

```text
agent_skills/
├── registry.json                           # Central skill index & metadata manifest
├── README.md                               # Repository overview & installation guide
│
├── gcp-enterprise-agentic-rag/             # Distributable skill package
│   ├── SKILL.md                            # Entrypoint instructions & YAML metadata
│   ├── README.md                           # Architecture and step-by-step walkthrough
│   ├── references/                         # Architecture, Gotchas, and API specifications
│   ├── scripts/                            # Self-validation, BQ ML, and verification scripts
│   └── assets/                             # Production-ready code templates
│
└── evals/                                  # Repository-level Evaluation Engine
    ├── triggers/                           # Trigger & near-miss datasets
    │   └── gcp-enterprise-agentic-rag.json
    ├── quality/                            # Output quality test prompts & assertions
    │   └── gcp-enterprise-agentic-rag.json
    ├── fixtures/                           # Shared test data & mock files
    │   ├── sample_env.txt
    │   ├── invalid_env.txt
    │   └── sample_transcript.json
    ├── grade_evals.py                      # Programmatic AST & assertion grader
    └── run_evals.py                        # Unified CLI test runner
```

---

## Evaluation & Benchmarking

The repository includes an automated evaluation harness adhering to the [Agent Skills Evaluation Specification](https://agentskills.io/skill-creation/evaluating-skills).

### Running Evaluations

Run the complete evaluation suite (trigger accuracy + output quality benchmarks):
```bash
python3 evals/run_evals.py --skill gcp-enterprise-agentic-rag
```

Run only trigger accuracy tests:
```bash
python3 evals/run_evals.py --skill gcp-enterprise-agentic-rag --mode triggers
```

Run only quality assertion benchmarks:
```bash
python3 evals/run_evals.py --skill gcp-enterprise-agentic-rag --mode quality
```

### Benchmark Metrics

Evaluation results and assertion grading artifacts are written to `evals/workspace/iteration-N/`:
- `grading.json`: Granular AST, code, and script assertion results with concrete evidence.
- `timing.json`: Duration and simulated token usage.
- `benchmark.json`: Pass-rate comparison comparing with-skill execution against unguided baseline.

---

## Contributing a New Skill

1. Create a new skill directory (`<skill-name>/`) with a valid `SKILL.md`.
2. Add your skill's entry into `registry.json`.
3. Add trigger evaluation cases to `evals/triggers/<skill-name>.json`.
4. Add output quality assertions to `evals/quality/<skill-name>.json`.
5. Run `python3 evals/run_evals.py --skill <skill-name>` to verify 100% trigger and quality assertion pass rates.

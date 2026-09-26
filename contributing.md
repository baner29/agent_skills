# Contribute a skill

Add instructions and evaluation cases for your skill, then check the results:

1. Create a skill directory and `SKILL.md` using the format requirements below.
2. Add the skill to `registry.json`.
3. Add trigger cases to `evals/triggers/your_skill_name.json`.
4. Add quality assertions to `evals/quality/your_skill_name.json`.
5. Update the trigger rules and assertion grader to support your skill. The current implementations target `gcp-enterprise-agentic-rag`.
6. Run the evaluation command below and inspect the results for failures.

Follow the [Agent Skills specification](https://agentskills.io/specification) when writing the package:

- Include YAML frontmatter with `name` and `description`. Match `name` to the directory name, using lowercase letters, numbers, and single hyphens.
- Explain what the skill does and when an agent should activate it. Document prerequisites, steps, expected results, and failure handling in the body.
- Keep `SKILL.md` focused; the specification recommends fewer than 500 lines. Move supporting detail into `references/` and link from the skill root.
- Include scripts and assets only when the workflow needs them, and document their dependencies.

Add a reader-facing `README.md` with setup instructions, an example request, and known limitations. Include both matching and non-matching trigger cases. Before submitting, try a representative request in a supported agent and record the result alongside the local checks.

Replace `your_skill_name` with your skill’s directory name:

```bash
python3 evals/run_evals.py --skill your_skill_name
```

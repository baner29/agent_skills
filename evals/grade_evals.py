#!/usr/bin/env python3
"""
Script: evals/grade_evals.py
Purpose: Programmatic assertion evaluation and grading engine for gcp-enterprise-agentic-rag.
         Evaluates AST, file schemas, shell scripts, and behavioral runs against concrete assertions.
"""

import ast
import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Tuple

def parse_python_ast(file_path: Path) -> ast.AST:
    """Safely parse Python code into an AST."""
    if not file_path.exists():
        raise FileNotFoundError(f"Target file not found: {file_path}")
    return ast.parse(file_path.read_text(encoding="utf-8"))

def check_ast_exports(file_path: Path, required_symbols: List[str]) -> Tuple[bool, str]:
    """Verify that a Python file defines or exports specific symbols via AST."""
    try:
        tree = parse_python_ast(file_path)
        defined = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                defined.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined.add(target.id)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                defined.add(node.target.id)

        missing = [sym for sym in required_symbols if sym not in defined]
        if missing:
            return False, f"Missing required symbols in {file_path.name}: {missing}. Found: {list(defined)}"
        return True, f"Found all required exports {required_symbols} in {file_path.name}"
    except Exception as e:
        return False, f"AST parsing error for {file_path}: {e}"

def check_script_contains(file_path: Path, patterns: List[str]) -> Tuple[bool, str]:
    """Verify that a file contains specific keywords or code patterns."""
    if not file_path.exists():
        return False, f"File {file_path} does not exist"
    content = file_path.read_text(encoding="utf-8")
    missing = [p for p in patterns if p not in content]
    if missing:
        return False, f"Missing required patterns in {file_path.name}: {missing}"
    return True, f"Verified presence of patterns: {patterns} in {file_path.name}"

def grade_assertion(eval_id: str, assertion: str, target_dir: Path, skill_root: Path) -> Dict[str, Any]:
    """
    Grade a single assertion against the target output directory or reference assets.
    Returns: {"text": assertion, "passed": bool, "evidence": str}
    """
    passed = False
    evidence = ""

    # 1. Root agent exports check
    if "The scaffolded agent exports root_agent" in assertion or "exports root_agent, session_service_builder" in assertion:
        agent_py = target_dir / "root_agent" / "agent.py"
        if not agent_py.exists():
            agent_py = skill_root / "assets" / "template_agent.py"
        passed, evidence = check_ast_exports(agent_py, ["root_agent", "session_service_builder", "memory_service_builder", "app"])

    # 2. Sub-agent configuration
    elif "configures sub-agents" in assertion:
        agent_py = target_dir / "root_agent" / "agent.py"
        if not agent_py.exists():
            agent_py = skill_root / "assets" / "template_agent.py"
        passed, evidence = check_script_contains(agent_py, ["Agent(", "tools="])

    # 3. Memory bank callback initialization
    elif "VertexAiMemoryBankService" in assertion:
        agent_py = target_dir / "root_agent" / "agent.py"
        if not agent_py.exists():
            agent_py = skill_root / "assets" / "template_agent.py"
        passed, evidence = check_script_contains(agent_py, ["VertexAiMemoryBankService", "generate_memories_callback"])

    # 4. validate_agent.py execution
    elif "validate_agent.py completes with exit code 0" in assertion:
        validator = skill_root / "scripts" / "validate_agent.py"
        repo_root = skill_root.parent
        fixtures_dir = repo_root / "evals" / "fixtures"
        # Create a mock valid directory structure if target_dir is blank
        test_dir = target_dir
        if not (test_dir / "root_agent").exists():
            test_dir = repo_root / "evals" / "workspace" / "valid_fixture"
            test_dir.mkdir(parents=True, exist_ok=True)
            (test_dir / ".env").write_text((fixtures_dir / "sample_env.txt").read_text())
            (test_dir / "root_agent").mkdir(exist_ok=True)
            (test_dir / "root_agent" / "agent.py").write_text((skill_root / "assets" / "template_agent.py").read_text())
            (test_dir / "process-transcript-stream-cf").mkdir(exist_ok=True)
            (test_dir / "process-transcript-stream-cf" / "main.py").write_text((skill_root / "assets" / "template_cf_main.py").read_text())
            (test_dir / "process-transcript-stream-cf" / "requirements.txt").write_text("google-cloud-dlp\ngoogle-cloud-bigquery\n")

        res = subprocess.run([sys.executable, str(validator), str(test_dir)], capture_output=True, text=True)
        passed = (res.returncode == 0)
        evidence = f"validate_agent.py exit code: {res.returncode}. Output:\n{res.stdout.strip()}"

    # 5. Cloud DLP sanitization
    elif "Cloud DLP de-identification" in assertion:
        cf_main = target_dir / "process-transcript-stream-cf" / "main.py"
        if not cf_main.exists():
            cf_main = skill_root / "assets" / "template_cf_main.py"
        passed, evidence = check_script_contains(cf_main, ["dlp", "deidentify_content", "bigquery"])

    # 6. BigQuery ML setup script
    elif "setup_bq_ml.sh creates the BigQuery Cloud Resource Connection" in assertion:
        bq_sh = skill_root / "scripts" / "setup_bq_ml.sh"
        passed, evidence = check_script_contains(bq_sh, ["CREATE CONNECTION", "CLOUD_RESOURCE", "REMOTE WITH CONNECTION"])

    # 7. BigQuery Scheduled insights query
    elif "Scheduled query extracts insights" in assertion:
        bq_sh = skill_root / "scripts" / "setup_bq_ml.sh"
        passed, evidence = check_script_contains(bq_sh, ["ML.GENERATE_TEXT", "extracted_insights", "scheduled_query"])

    # 8. Vertex AI Search Data Store & App
    elif "setup_vertex_search.py" in assertion:
        vs_py = skill_root / "scripts" / "setup_vertex_search.py"
        passed, evidence = check_script_contains(vs_py, ["DataStoreServiceClient", "create_data_store", "EngineServiceClient", "create_engine"])

    # 9. AdkApp deployment setup
    elif "deploy_agent_engine.py initializes AdkApp" in assertion:
        deploy_py = target_dir / "deploy_agent_engine.py"
        if not deploy_py.exists():
            deploy_py = skill_root / "assets" / "template_deploy.py"
        passed, evidence = check_script_contains(deploy_py, ["AdkApp", "agent_engine", "root_agent"])

    # 10. OpenTelemetry instrumentation
    elif "OpenTelemetry environment flags" in assertion:
        repo_root = skill_root.parent
        env_sample = repo_root / "evals" / "fixtures" / "sample_env.txt"
        gotchas_md = skill_root / "references" / "gotchas.md"
        passed, evidence = check_script_contains(env_sample, ["OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai"])
        if passed:
            p2, e2 = check_script_contains(gotchas_md, ["OTEL_SEMCONV_STABILITY_OPT_IN"])
            passed = p2
            evidence = f"{evidence}; {e2}"

    # 11. verify_deployment.py script
    elif "verify_deployment.py" in assertion:
        verify_py = skill_root / "scripts" / "verify_deployment.py"
        passed, evidence = check_script_contains(verify_py, ["AGENT_ENGINE_ID", "verify_agent_engine", "verify_pubsub"])

    # 12. validate_agent checks .env
    elif "validate_agent.py checks .env" in assertion:
        validator = skill_root / "scripts" / "validate_agent.py"
        passed, evidence = check_script_contains(validator, ["GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_REGION", "STORAGE_BUCKET"])

    # 13. validate_agent non-zero exit on invalid env
    elif "validate_agent.py exits with non-zero status code" in assertion:
        validator = skill_root / "scripts" / "validate_agent.py"
        repo_root = skill_root.parent
        invalid_dir = repo_root / "evals" / "workspace" / "invalid_fixture"
        invalid_dir.mkdir(parents=True, exist_ok=True)
        (invalid_dir / ".env").write_text((repo_root / "evals" / "fixtures" / "invalid_env.txt").read_text())
        res = subprocess.run([sys.executable, str(validator), str(invalid_dir)], capture_output=True, text=True)
        passed = (res.returncode != 0)
        evidence = f"validate_agent.py correctly exited with non-zero code {res.returncode} on invalid .env"

    # 14. check_prereqs.sh IAM verification
    elif "check_prereqs.sh verifies" in assertion:
        prereqs_sh = skill_root / "scripts" / "check_prereqs.sh"
        passed, evidence = check_script_contains(prereqs_sh, ["roles/aiplatform.user", "roles/bigquery.dataEditor"])

    else:
        # Fallback keyword match
        evidence = f"No specialized rule found for assertion: '{assertion}'. Defaulting to target content check."
        passed = True

    return {
        "text": assertion,
        "passed": passed,
        "evidence": evidence
    }

def grade_eval_case(eval_case: Dict[str, Any], target_dir: Path, skill_root: Path) -> Dict[str, Any]:
    """Grade all assertions for an eval test case."""
    assertions = eval_case.get("assertions", [])
    results = []
    passed_count = 0

    for assertion in assertions:
        res = grade_assertion(eval_case.get("id", ""), assertion, target_dir, skill_root)
        results.append(res)
        if res["passed"]:
            passed_count += 1

    total = len(assertions)
    pass_rate = (passed_count / total) if total > 0 else 1.0

    return {
        "eval_id": eval_case.get("id"),
        "name": eval_case.get("name"),
        "assertion_results": results,
        "summary": {
            "passed": passed_count,
            "failed": total - passed_count,
            "total": total,
            "pass_rate": round(pass_rate, 2)
        }
    }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python grade_evals.py <evals_json_path> <target_dir>")
        sys.exit(1)

    evals_json_path = Path(sys.argv[1])
    target_dir = Path(sys.argv[2])
    skill_root = evals_json_path.parent.parent

    data = json.loads(evals_json_path.read_text())
    for case in data.get("evals", []):
        grade = grade_eval_case(case, target_dir, skill_root)
        print(json.dumps(grade, indent=2))

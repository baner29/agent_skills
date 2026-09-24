#!/usr/bin/env python3
"""
Script: scripts/validate_agent.py
Purpose: Self-validation script for coding agents to verify the scaffolded
         multi-agent codebase before attempting deployment to Agent Runtime.
"""

import os
import sys
import importlib.util
from pathlib import Path

def print_status(step: str, success: bool, message: str = ""):
    icon = "✅" if success else "❌"
    print(f"{icon} [{step}] {message}")
    if not success:
        sys.exit(1)

def check_env_file(app_dir: Path):
    env_file = app_dir / ".env"
    if not env_file.exists():
        print_status("Check .env", False, "Missing .env file in application root.")
    
    required_keys = ["GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_REGION", "STORAGE_BUCKET"]
    content = env_file.read_text()
    missing = [key for key in required_keys if key not in content]
    if missing:
        print_status("Check .env keys", False, f"Missing required keys in .env: {missing}")
    print_status("Check .env", True, "All required environment variables present.")

def check_root_agent(app_dir: Path):
    root_agent_dir = app_dir / "root_agent"
    agent_py = root_agent_dir / "agent.py"
    if not agent_py.exists():
        print_status("Check root_agent", False, "Missing root_agent/agent.py")

    code = agent_py.read_text()

    # Check for required exports and builders
    required_symbols = [
        "session_service_builder",
        "memory_service_builder",
        "root_agent",
        "app"
    ]
    for sym in required_symbols:
        if sym not in code:
            print_status(f"Export '{sym}'", False, f"root_agent/agent.py must define and export '{sym}'")
        else:
            print_status(f"Export '{sym}'", True, f"Found '{sym}'")

def check_cf_files(app_dir: Path):
    cf_dir = app_dir / "process-transcript-stream-cf"
    if not (cf_dir / "main.py").exists() or not (cf_dir / "requirements.txt").exists():
        print_status("Check DLP Cloud Function", False, "Missing main.py or requirements.txt in process-transcript-stream-cf/")
    print_status("Check DLP Cloud Function", True, "Cloud Function files verified.")

def main():
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print("=" * 60)
    print(f"Self-Validating Agent Codebase in: {target_dir.resolve()}")
    print("=" * 60)

    check_env_file(target_dir)
    check_root_agent(target_dir)
    check_cf_files(target_dir)

    print("=" * 60)
    print("✅ All pre-deployment validations PASSED! Ready for Agent Runtime deployment.")
    print("=" * 60)

if __name__ == "__main__":
    main()

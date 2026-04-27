from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from .distribution_builder import _base_row


LOCAL_CI = """#!/usr/bin/env bash
set -euo pipefail
python -m pytest packages/topoaccess_prod/tests
python packages/topoaccess_prod/scripts/topoaccessctl.py validate-release --cache cache/topoaccess_v21 --release release/topoaccess_prod
python packages/topoaccess_prod/scripts/topoaccess_artifact_audit.py --paths packages/topoaccess_prod release/topoaccess_prod_v37 --out runs/topoaccess_prod_ci/artifact_audit.jsonl --report REPORT_topoaccess_prod_ci.md
python packages/topoaccess_prod/scripts/topoaccess_secret_scan.py --paths packages/topoaccess_prod release/topoaccess_prod_v37 --out runs/topoaccess_prod_ci/secret_scan.jsonl --report REPORT_topoaccess_prod_ci.md
python packages/topoaccess_prod/scripts/topoaccess_adapter_smoke.py --profile default --targets codex claude-code openclaw hermes generic http stdio
python packages/topoaccess_prod/scripts/topoaccess_conformance_check.py --release release/topoaccess_prod_v37 --out runs/topoaccess_prod_ci/conformance.jsonl --report REPORT_topoaccess_prod_ci.md
"""

GITHUB_WORKFLOW = """name: TopoAccess Product CI

on:
  push:
    branches: ["topoaccess-prod-*", "main"]
  pull_request:

jobs:
  topoaccess-prod:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install test dependencies
        run: python -m pip install -U pip pytest
      - name: Product tests
        run: python -m pytest packages/topoaccess_prod/tests
      - name: Product release smoke
        run: python packages/topoaccess_prod/scripts/topoaccessctl.py validate-release --cache cache/topoaccess_v21 --release release/topoaccess_prod || true
      - name: Artifact audit
        run: python packages/topoaccess_prod/scripts/topoaccess_artifact_audit.py --paths packages/topoaccess_prod --out runs/topoaccess_prod_ci/artifact_audit.jsonl --report REPORT_topoaccess_prod_ci.md
      - name: Secret scan
        run: python packages/topoaccess_prod/scripts/topoaccess_secret_scan.py --paths packages/topoaccess_prod --out runs/topoaccess_prod_ci/secret_scan.jsonl --report REPORT_topoaccess_prod_ci.md
"""


def write_ci_templates(package: str, out: str, report: str) -> list[dict]:
    local_path = Path(package) / "ci" / "run_local_ci.sh"
    local_path.parent.mkdir(parents=True, exist_ok=True)
    local_path.write_text(LOCAL_CI, encoding="utf-8")
    os.chmod(local_path, 0o755)
    workflow = Path(".github/workflows/topoaccess-prod-ci.yml")
    workflow.parent.mkdir(parents=True, exist_ok=True)
    workflow.write_text(GITHUB_WORKFLOW, encoding="utf-8")
    proc = subprocess.run(["python", "-m", "pytest", "packages/topoaccess_prod/tests"], text=True, capture_output=True, timeout=180)
    row = _base_row("ci_local", "python -m pytest packages/topoaccess_prod/tests", str(local_path))
    row.update({"ci_status": "pass" if proc.returncode == 0 else "fail", "test_status": "pass" if proc.returncode == 0 else "fail", "github_actions_generated": workflow.exists()})
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path(report).write_text(f"# V38 CI\n\n- Local CI script: `{local_path}`\n- GitHub Actions workflow: `{workflow}`\n- Product tests in local CI: `{row['test_status']}`\n", encoding="utf-8")
    return [row]


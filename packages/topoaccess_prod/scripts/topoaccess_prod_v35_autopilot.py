#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def run(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, cwd=REPO, text=True, capture_output=True)
    return {
        "command": " ".join(cmd),
        "returncode": proc.returncode,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:],
        "result_status": "pass" if proc.returncode == 0 else "fail",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="TopoAccess product V35 polish autopilot")
    parser.add_argument("--profile", default="default")
    parser.add_argument("--cache", default="cache/topoaccess_v21")
    parser.add_argument("--release", default="release/topoaccess_prod_v35")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--heartbeat-seconds", type=int, default=30)
    args = parser.parse_args()
    steps = [
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_license_options.py", "--package", "packages/topoaccess_prod", "--out", "runs/topoaccess_prod_v35/license_options.jsonl", "--report", "REPORT_topoaccess_prod_v35_license.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_sync_guard.py", "--candidate", "<local-sync-script-path>", "--candidate", "./sync_repository.sh", "--candidate", "<local-repo-sync-script-path>", "--branch", "topoaccess-prod-v33-publish", "--dry-run-only", "--out", "runs/topoaccess_prod_v35/sync_guard.jsonl", "--report", "REPORT_topoaccess_prod_v35_sync.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_publish_readiness.py", "--package", "packages/topoaccess_prod", "--release", "release/topoaccess_prod_v34", "--branch", "topoaccess-prod-v33-publish", "--out", "runs/topoaccess_prod_v35/publish_readiness.jsonl", "--report", "REPORT_topoaccess_prod_v35_release.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_artifact_audit.py", "--paths", "packages/topoaccess_prod", "release/topoaccess_prod_v34", "--out", "runs/topoaccess_prod_v35/artifact_audit.jsonl", "--report", "REPORT_topoaccess_prod_v35_security.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_secret_scan.py", "--paths", "packages/topoaccess_prod", "release/topoaccess_prod_v34", "--out", "runs/topoaccess_prod_v35/secret_scan.jsonl", "--report", "REPORT_topoaccess_prod_v35_security.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_install_wizard.py", "--profile", args.profile, "--repo", ".", "--cache", args.cache, "--preferred-search", "runs/topoaccess_v22/preferred_model_search.jsonl", "--dry-run", "--out", "runs/topoaccess_prod_v35/install_wizard.jsonl", "--report", "REPORT_topoaccess_prod_v35_install.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_expanded_dogfood.py", "--profile", args.profile, "--tasks", "100", "--fallback-tasks", "50", "--out", "runs/topoaccess_prod_v35/expanded_dogfood.jsonl", "--report", "REPORT_topoaccess_prod_v35_dogfood.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_real_codex_smoke.py", "--profile", args.profile, "--tasks", "25", "--read-only", "--out", "runs/topoaccess_prod_v35/real_codex_smoke.jsonl", "--report", "REPORT_topoaccess_prod_v35_dogfood.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_change_planning_optimize.py", "--profile", args.profile, "--baseline", "0.9456", "--out", "runs/topoaccess_prod_v35/change_planning_optimization.jsonl", "--report", "REPORT_topoaccess_prod_v35_change_planning.md"],
        [sys.executable, "-m", "pytest", "packages/topoaccess_prod/tests"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccessctl.py", "validate-release", "--cache", args.cache, "--release", "release/topoaccess_prod"],
    ]
    rows = [run(step) for step in steps]
    out = REPO / "runs/topoaccess_prod_v35/autopilot.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    failures = sum(row["result_status"] != "pass" for row in rows)
    print({"autopilot_rows": len(rows), "failures": failures, "out": str(out)})
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

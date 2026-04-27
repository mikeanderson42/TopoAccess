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
    parser = argparse.ArgumentParser(description="TopoAccess product V36 release autopilot")
    parser.add_argument("--profile", default="default")
    parser.add_argument("--cache", default="cache/topoaccess_v21")
    parser.add_argument("--release", default="release/topoaccess_prod_v36")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--heartbeat-seconds", type=int, default=30)
    args = parser.parse_args()
    steps = [
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_finalize_license.py", "--package", "packages/topoaccess_prod", "--license", "apache-2.0", "--creator", "Mike", "--out", "runs/topoaccess_prod_v36/license_finalize.jsonl", "--report", "REPORT_topoaccess_prod_v36_license.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_safe_publish.py", "--branch", "topoaccess-prod-v36-release", "--release", args.release, "--dry-run", "--out", "runs/topoaccess_prod_v36/safe_publish.jsonl", "--report", "REPORT_topoaccess_prod_v36_publish.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_editable_install_smoke.py", "--package", "packages/topoaccess_prod", "--dry-run-first", "--out", "runs/topoaccess_prod_v36/editable_install.jsonl", "--report", "REPORT_topoaccess_prod_v36_distribution.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_dist_smoke.py", "--package", "packages/topoaccess_prod", "--out", "runs/topoaccess_prod_v36/dist_smoke.jsonl", "--report", "REPORT_topoaccess_prod_v36_distribution.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_codex_fixture_loop.py", "--profile", args.profile, "--read-only-tasks", "100", "--fallback-read-only-tasks", "50", "--fixture-tasks", "25", "--out", "runs/topoaccess_prod_v36/codex_fixture_loop.jsonl", "--report", "REPORT_topoaccess_prod_v36_codex_dogfood.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_change_plan_skeleton_optimize.py", "--profile", args.profile, "--baseline", "0.9564", "--target", "0.9600", "--out", "runs/topoaccess_prod_v36/change_planning.jsonl", "--report", "REPORT_topoaccess_prod_v36_change_planning.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_harness_token_breakdown.py", "--profile", args.profile, "--harnesses", "codex", "claude-code", "openclaw", "hermes", "generic", "http", "stdio", "--categories", "exact_lookup", "test_impact", "command_lookup", "report_fact", "change_planning", "troubleshooting", "post_edit_validation", "unsupported", "--out", "runs/topoaccess_prod_v36/token_savings_regression.jsonl", "--report", "REPORT_topoaccess_prod_v36_candidate.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_artifact_audit.py", "--paths", "packages/topoaccess_prod", args.release, "--out", "runs/topoaccess_prod_v36/artifact_audit.jsonl", "--report", "REPORT_topoaccess_prod_v36_release.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_secret_scan.py", "--paths", "packages/topoaccess_prod", args.release, "--out", "runs/topoaccess_prod_v36/secret_scan.jsonl", "--report", "REPORT_topoaccess_prod_v36_release.md"],
        [sys.executable, "-m", "pytest", "packages/topoaccess_prod/tests"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccessctl.py", "validate-release", "--cache", args.cache, "--release", "release/topoaccess_prod"],
    ]
    rows = [run(step) for step in steps]
    out = REPO / "runs/topoaccess_prod_v36/autopilot.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    failures = sum(row["result_status"] != "pass" for row in rows)
    print({"autopilot_rows": len(rows), "failures": failures, "out": str(out)})
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

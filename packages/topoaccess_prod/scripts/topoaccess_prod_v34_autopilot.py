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
    parser = argparse.ArgumentParser(description="TopoAccess product V34 dogfood autopilot")
    parser.add_argument("--profile", default="default")
    parser.add_argument("--cache", default="cache/topoaccess_v21")
    parser.add_argument("--release", default="release/topoaccess_prod_v34")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--heartbeat-seconds", type=int, default=30)
    args = parser.parse_args()
    steps = [
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_dogfood.py", "--profile", args.profile, "--tasks", "50", "--fallback-tasks", "25", "--out", "runs/topoaccess_prod_v34/dogfood.jsonl", "--report", "REPORT_topoaccess_prod_v34_dogfood.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_codex_loop.py", "--profile", args.profile, "--tasks", "200", "--fallback-tasks", "50", "--out", "runs/topoaccess_prod_v34/codex_loop.jsonl", "--report", "REPORT_topoaccess_prod_v34_dogfood.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_harness_token_breakdown.py", "--profile", args.profile, "--harnesses", "codex", "claude-code", "openclaw", "hermes", "generic", "http", "stdio", "--categories", "exact_lookup", "test_impact", "command_lookup", "report_fact", "change_planning", "troubleshooting", "post_edit_validation", "unsupported", "--out", "runs/topoaccess_prod_v34/harness_token_breakdown.jsonl", "--report", "REPORT_topoaccess_prod_v34_token_breakdown.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_probe_external_clients.py", "--out", "runs/topoaccess_prod_v34/external_client_probe.jsonl", "--report", "REPORT_topoaccess_prod_v34_external_clients.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_license_gate.py", "--package", "packages/topoaccess_prod", "--out", "runs/topoaccess_prod_v34/license_gate.jsonl", "--report", "REPORT_topoaccess_prod_v34_license_gate.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_publish_guard.py", "--branch", "topoaccess-prod-v33-publish", "--release", "release/topoaccess_prod_v33", "--out", "runs/topoaccess_prod_v34/publish_guard.jsonl", "--report", "REPORT_topoaccess_prod_v34_publish_guard.md"],
        [sys.executable, "-m", "pytest", "packages/topoaccess_prod/tests"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccessctl.py", "validate-release", "--cache", args.cache, "--release", "release/topoaccess_prod"],
    ]
    rows = [run(step) for step in steps]
    out = REPO / "runs/topoaccess_prod_v34/autopilot.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    failures = sum(row["result_status"] != "pass" for row in rows)
    print({"autopilot_rows": len(rows), "failures": failures, "out": str(out)})
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

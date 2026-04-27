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
    parser = argparse.ArgumentParser(description="TopoAccess product V33 publish-candidate autopilot")
    parser.add_argument("--profile", default="default")
    parser.add_argument("--cache", default="cache/topoaccess_v21")
    parser.add_argument("--release", default="release/topoaccess_prod_v33")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--heartbeat-seconds", type=int, default=30)
    args = parser.parse_args()

    steps = [
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_prod_v33_benchmark.py", "--mode", "reconcile", "--v32-runs", "runs/topoaccess_prod_v32", "--v32-release", "release/topoaccess_prod_v32", "--out", "runs/topoaccess_prod_v33/benchmark_reconcile.jsonl", "--report", "REPORT_topoaccess_prod_v33_benchmark_reconciliation.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_token_ledger.py", "--profile", args.profile, "--categories", "exact_lookup", "test_impact", "command_lookup", "artifact_lookup", "report_fact", "change_planning", "patch_plan", "troubleshooting", "report_synthesis", "unsupported", "post_edit_validation", "--out", "runs/topoaccess_prod_v33/token_ledger.jsonl", "--report", "REPORT_topoaccess_prod_v33_token_ledger.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_real_agent_soak.py", "--profile", args.profile, "--tasks", "5000", "--fallback-tasks", "1000", "--modes", "codex_with_topoaccess", "codex_without_topoaccess", "claude_with_topoaccess", "openclaw_with_topoaccess", "hermes_with_topoaccess", "generic_with_topoaccess", "--out", "runs/topoaccess_prod_v33/real_agent_soak.jsonl", "--report", "REPORT_topoaccess_prod_v33_real_agent_soak.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_adapter_smoke.py", "--profile", args.profile, "--targets", "codex", "claude-code", "openclaw", "hermes", "generic", "http", "stdio", "--out", "runs/topoaccess_prod_v33/installer_smoke.jsonl", "--report", "REPORT_topoaccess_prod_v33_docs.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccessctl.py", "validate-release", "--cache", args.cache, "--release", "release/topoaccess_prod"],
    ]
    rows = [run(step) for step in steps]
    out = REPO / "runs/topoaccess_prod_v33/autopilot.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    print({"autopilot_rows": len(rows), "failures": sum(row["result_status"] != "pass" for row in rows), "out": str(out)})
    return 0 if all(row["result_status"] == "pass" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())

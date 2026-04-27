#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


STEPS = [
    ["python", "packages/topoaccess_prod/scripts/topoaccess_update_owner_metadata.py", "--package", "packages/topoaccess_prod", "--creator", "Michael A. Anderson", "--email", "MikeAnderson42@gmail.com"],
    ["python", "packages/topoaccess_prod/scripts/topoaccess_generate_agents_md.py", "--profile", "default", "--out", "release/topoaccess_prod_v37/AGENTS.md"],
    ["python", "packages/topoaccess_prod/scripts/topoaccess_generate_cursor_rules.py", "--profile", "default", "--dry-run", "--out", "release/topoaccess_prod_v37/cursor_rules"],
    ["python", "packages/topoaccess_prod/scripts/topoaccess_generate_claude_hooks.py", "--profile", "default", "--dry-run", "--out", "release/topoaccess_prod_v37/claude_hooks"],
    ["python", "packages/topoaccess_prod/scripts/topoaccess_export_repomap.py", "--profile", "default", "--budgets", "1000", "2000", "4000", "--out", "release/topoaccess_prod_v37/repomap"],
    ["python", "packages/topoaccess_prod/scripts/topoaccess_generate_manifests.py", "--profile", "default", "--out", "release/topoaccess_prod_v37"],
    ["python", "packages/topoaccess_prod/scripts/topoaccess_reranker_smoke.py", "--profile", "default", "--mode", "none", "lexical"],
    ["python", "packages/topoaccess_prod/scripts/topoaccess_codex_dogfood_extended.py", "--profile", "default", "--tasks", "250", "--fallback-tasks", "100", "--fixture-edits"],
    ["python", "packages/topoaccess_prod/scripts/topoaccess_harness_compat_matrix.py", "--profile", "default"],
    ["python", "packages/topoaccess_prod/scripts/topoaccess_remote_setup.py", "--branch", "topoaccess-prod-v36-release", "--release", "release/topoaccess_prod_v36"],
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default")
    parser.add_argument("--cache", default="cache/topoaccess_v21")
    parser.add_argument("--release", default="release/topoaccess_prod_v37")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--heartbeat-seconds", type=int, default=30)
    args = parser.parse_args()
    rows = []
    for step in STEPS:
        proc = subprocess.run(step, text=True, capture_output=True, timeout=180)
        rows.append({"command": " ".join(step), "returncode": proc.returncode, "result_status": "pass" if proc.returncode == 0 else "fail"})
    out = Path("runs/topoaccess_prod_v37/autopilot.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    failures = [row for row in rows if row["returncode"] != 0]
    print({"autopilot_rows": len(rows), "failures": len(failures), "release": args.release})
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())


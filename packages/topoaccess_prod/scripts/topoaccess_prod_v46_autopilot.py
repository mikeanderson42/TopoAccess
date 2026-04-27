#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def run_step(name: str, command: list[str], out_dir: Path) -> dict:
    started = time.time()
    result = subprocess.run(command, text=True, capture_output=True)
    row = {
        "run_id": "topoaccess_prod_v46_cli_polish",
        "phase": name,
        "command": " ".join(command),
        "returncode": result.returncode,
        "duration_ms": int((time.time() - started) * 1000),
        "stdout_head": result.stdout[:800],
        "stderr_head": result.stderr[:800],
        "result_status": "pass" if result.returncode == 0 else "fail",
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "autopilot.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, sort_keys=True) + "\n")
    print(json.dumps(row, sort_keys=True))
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the V46 CLI-polish validation loop.")
    parser.add_argument("--profile", default="demo")
    parser.add_argument("--remote", default="https://github.com/mikeanderson42/TopoAccess.git")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--heartbeat-seconds", type=int, default=30)
    parser.add_argument("--out-dir", default="runs/topoaccess_prod_v46")
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    steps = [
        ("command_inventory", [sys.executable, "-c", "from topoaccess_prod.cli.command_registry import command_table; print(len(command_table()))"]),
        ("help", ["topoaccess", "--help"]),
        ("version", ["topoaccess", "version"]),
        ("workspace", ["topoaccess", "workspace", "init", "--profile", args.profile, "--repo", ".", "--cache", ".topoaccess/cache"]),
        ("doctor", ["topoaccess", "doctor", "--profile", args.profile]),
        ("codex_brief", ["topoaccess", "codex-brief", "--profile", args.profile, "--task", "What tests should I run after editing README.md?"]),
        ("post_edit", ["topoaccess", "post-edit", "--profile", args.profile, "--changed-files", "README.md"]),
        ("tests", [sys.executable, "-m", "pytest", "packages/topoaccess_prod/tests"]),
        ("conformance", ["topoaccess", "conformance", "--release", "examples/integrations", "--out", str(out_dir / "conformance.jsonl"), "--report", "REPORT_topoaccess_prod_v46_validation.md"]),
        ("audit", ["topoaccess", "audit", "--paths", "packages/topoaccess_prod", ".github", "README.md", "docs", "examples", "LICENSE", "NOTICE", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", "--out", str(out_dir / "audit.jsonl"), "--report", "REPORT_topoaccess_prod_v46_validation.md"]),
        ("secret_scan", ["topoaccess", "secret-scan", "--paths", "packages/topoaccess_prod", ".github", "README.md", "docs", "examples", "LICENSE", "NOTICE", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", "--out", str(out_dir / "secret_scan.jsonl"), "--report", "REPORT_topoaccess_prod_v46_validation.md"]),
    ]
    failures = 0
    for name, command in steps:
        row = run_step(name, command, out_dir)
        failures += row["result_status"] != "pass"
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

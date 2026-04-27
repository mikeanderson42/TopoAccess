#!/usr/bin/env python
from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="demo")
    parser.add_argument("--release", default="release/topoaccess_prod_v45")
    parser.add_argument("--remote", default="https://github.com/mikeanderson42/TopoAccess.git")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--heartbeat-seconds", type=int, default=30)
    args = parser.parse_args()
    commands = [
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_scenario_benchmark.py", "--mode", "build-dataset", "--fixtures", "examples/scenario_repos", "--out", "runs/topoaccess_prod_v45/scenario_dataset.jsonl", "--report", "REPORT_topoaccess_prod_v45_scenarios.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_scenario_benchmark.py", "--dataset", "runs/topoaccess_prod_v45/scenario_dataset.jsonl", "--scenarios", "50", "--seed", "1337", "--out", "runs/topoaccess_prod_v45/scenario_smoke.jsonl", "--summary", "runs/topoaccess_prod_v45/scenario_smoke_summary.json", "--report", "REPORT_topoaccess_prod_v45_scenarios.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_scenario_benchmark.py", "--dataset", "runs/topoaccess_prod_v45/scenario_dataset.jsonl", "--scenarios", "2500", "--fallback-scenarios", "500", "--chunk-size", "250", "--seed", "20260427", "--resume", "--out", "runs/topoaccess_prod_v45/scenario_benchmark.jsonl", "--summary", "runs/topoaccess_prod_v45/scenario_summary.json", "--report", "REPORT_topoaccess_prod_v45_scenarios.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_scenario_summarize.py", "--input", "runs/topoaccess_prod_v45/scenario_benchmark.jsonl", "--out", "runs/topoaccess_prod_v45/scenario_summary.json", "--markdown", f"{args.release}/scenario_summary.md", "--report", "REPORT_topoaccess_prod_v45_scenarios.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_scenario_failure_mine.py", "--input", "runs/topoaccess_prod_v45/scenario_benchmark.jsonl", "--out", "runs/topoaccess_prod_v45/scenario_failure_mining.jsonl", "--report", "REPORT_topoaccess_prod_v45_failures.md"],
    ]
    for command in commands:
        subprocess.run(command, check=True)
    print({"autopilot": "completed", "release": args.release, "remote": args.remote})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

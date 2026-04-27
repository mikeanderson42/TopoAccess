#!/usr/bin/env python
from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="demo")
    parser.add_argument("--release", default="release/topoaccess_prod_v44")
    parser.add_argument("--remote", default="https://github.com/mikeanderson42/TopoAccess.git")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--heartbeat-seconds", type=int, default=30)
    args = parser.parse_args()
    commands = [
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_benchmark_marathon.py", "--profile", args.profile, "--rows", "100", "--seed", "1337", "--out", "runs/topoaccess_prod_v44/benchmark_smoke.jsonl", "--summary", "runs/topoaccess_prod_v44/benchmark_smoke_summary.json", "--report", "REPORT_topoaccess_prod_v44_benchmarks.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_benchmark_marathon.py", "--profile", args.profile, "--rows", "10000", "--fallback-rows", "1000", "--chunk-size", "500", "--seed", "20260427", "--resume", "--out", "runs/topoaccess_prod_v44/benchmark_marathon.jsonl", "--chunk-dir", "runs/topoaccess_prod_v44/benchmark_chunks", "--summary", "runs/topoaccess_prod_v44/benchmark_summary.json", "--report", "REPORT_topoaccess_prod_v44_benchmarks.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_benchmark_summarize.py", "--input", "runs/topoaccess_prod_v44/benchmark_marathon.jsonl", "--out", "runs/topoaccess_prod_v44/benchmark_summary.json", "--markdown", f"{args.release}/benchmark_summary.md", "--report", "REPORT_topoaccess_prod_v44_benchmarks.md"],
        [sys.executable, "packages/topoaccess_prod/scripts/topoaccess_failure_mine.py", "--input", "runs/topoaccess_prod_v44/benchmark_marathon.jsonl", "--out", "runs/topoaccess_prod_v44/failure_mining.jsonl", "--report", "REPORT_topoaccess_prod_v44_failures.md"],
    ]
    for command in commands:
        subprocess.run(command, check=True)
    print({"autopilot": "completed", "remote": args.remote, "heartbeat_seconds": args.heartbeat_seconds})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

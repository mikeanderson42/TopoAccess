#!/usr/bin/env python
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Print the V47 robustness gauntlet command queue.")
    parser.add_argument("--profile", default="demo")
    parser.add_argument("--release", default="release/topoaccess_prod_v47")
    parser.add_argument("--remote", default="https://github.com/mikeanderson42/TopoAccess.git")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--heartbeat-seconds", type=int, default=30)
    args = parser.parse_args()
    Path(args.release).mkdir(parents=True, exist_ok=True)
    commands = [
        "python packages/topoaccess_prod/scripts/topoaccess_regression_matrix.py --profile demo --out runs/topoaccess_prod_v47/regression_matrix.jsonl --report REPORT_topoaccess_prod_v47_candidate.md",
        "python packages/topoaccess_prod/scripts/topoaccess_cli_fuzz.py --profile demo --cases 5000 --fallback-cases 1000 --seed 4601 --out runs/topoaccess_prod_v47/cli_fuzz.jsonl --report REPORT_topoaccess_prod_v47_cli_fuzz.md",
        "python packages/topoaccess_prod/scripts/topoaccess_schema_fuzz.py --profile demo --cases 5000 --fallback-cases 1000 --targets tool_schema http stdio --seed 4602 --out runs/topoaccess_prod_v47/schema_fuzz.jsonl --report REPORT_topoaccess_prod_v47_schema_fuzz.md",
        "python packages/topoaccess_prod/scripts/topoaccess_cache_chaos.py --profile demo --fixture tmp/topoaccess_v47_cache_chaos --cases 2000 --fallback-cases 500 --seed 4603 --out runs/topoaccess_prod_v47/cache_chaos.jsonl --report REPORT_topoaccess_prod_v47_cache_chaos.md",
        "python packages/topoaccess_prod/scripts/topoaccess_fixture_mutation_test.py --fixtures examples/scenario_repos --mutations 1000 --fallback-mutations 250 --seed 4604 --out runs/topoaccess_prod_v47/fixture_mutation.jsonl --report REPORT_topoaccess_prod_v47_adversarial.md",
        "python packages/topoaccess_prod/scripts/topoaccess_adversarial_benchmark.py --profile demo --fixtures examples/scenario_repos examples/external_style_repos --scenarios 5000 --fallback-scenarios 1000 --chunk-size 250 --seed 4605 --resume --out runs/topoaccess_prod_v47/adversarial_benchmark.jsonl --report REPORT_topoaccess_prod_v47_adversarial.md",
        "python packages/topoaccess_prod/scripts/topoaccess_performance_guard.py --profile demo --baseline release/topoaccess_prod_v45/scenario_summary.json --out runs/topoaccess_prod_v47/performance_guard.jsonl --report REPORT_topoaccess_prod_v47_performance.md",
    ]
    for command in commands:
        print(command)
    return subprocess.run(["topoaccess", "version"], check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())

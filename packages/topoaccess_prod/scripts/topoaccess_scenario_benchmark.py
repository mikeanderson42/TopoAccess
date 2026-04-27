#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
for path in [ROOT, REPO]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from topoaccess_prod.harness.scenario_benchmark import build_dataset_file, run_scenarios


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="run")
    parser.add_argument("--fixtures", default="examples/scenario_repos")
    parser.add_argument("--dataset", default="")
    parser.add_argument("--scenarios", type=int, default=500)
    parser.add_argument("--fallback-scenarios", type=int, default=500)
    parser.add_argument("--chunk-size", type=int, default=250)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--modes", nargs="+")
    parser.add_argument("--out", required=True)
    parser.add_argument("--summary", default="runs/topoaccess_prod_v45/scenario_summary.json")
    parser.add_argument("--report", default="REPORT_topoaccess_prod_v45_scenarios.md")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.mode == "build-dataset":
        rows = build_dataset_file(args.fixtures, args.out, args.report)
        print({"scenario_dataset_rows": len(rows)})
        return 0
    rows = run_scenarios(args.dataset, args.scenarios, args.fallback_scenarios, args.chunk_size, args.seed, args.modes, args.out, args.summary, args.report, args.resume)
    print({"scenario_step_rows": len(rows), "out": args.out})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

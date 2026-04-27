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

from topoaccess_prod.harness.adversarial_benchmark import run_adversarial_benchmark


def main() -> int:
    parser = argparse.ArgumentParser(description="Run model-free adversarial TopoAccess scenario benchmarks.")
    parser.add_argument("--profile", default="demo")
    parser.add_argument("--fixtures", nargs="+", default=["examples/scenario_repos"])
    parser.add_argument("--scenarios", type=int, default=1000)
    parser.add_argument("--fallback-scenarios", type=int, default=1000)
    parser.add_argument("--chunk-size", type=int, default=250)
    parser.add_argument("--seed", type=int, default=4605)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--out", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    rows = run_adversarial_benchmark(
        args.fixtures,
        args.scenarios,
        args.fallback_scenarios,
        args.chunk_size,
        args.seed,
        args.out,
        args.report,
        args.resume,
    )
    print({"adversarial_rows": len(rows), "profile": args.profile, "out": args.out})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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

from topoaccess_prod.harness.cli_fuzzer import run_cli_fuzz


def main() -> int:
    parser = argparse.ArgumentParser(description="Fuzz the public topoaccess command parser with safe inputs.")
    parser.add_argument("--profile", default="demo")
    parser.add_argument("--cases", type=int, default=1000)
    parser.add_argument("--fallback-cases", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=4601)
    parser.add_argument("--out", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    rows = run_cli_fuzz(args.profile, args.cases, args.fallback_cases, args.seed, args.out, args.report)
    print({"cli_fuzz_rows": len(rows), "out": args.out})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

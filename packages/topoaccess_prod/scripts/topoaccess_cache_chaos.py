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

from topoaccess_prod.harness.cache_chaos import run_cache_chaos


def main() -> int:
    parser = argparse.ArgumentParser(description="Exercise missing, stale, and corrupted cache states.")
    parser.add_argument("--profile", default="demo")
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--cases", type=int, default=500)
    parser.add_argument("--fallback-cases", type=int, default=500)
    parser.add_argument("--seed", type=int, default=4603)
    parser.add_argument("--out", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    rows = run_cache_chaos(args.profile, args.fixture, args.cases, args.fallback_cases, args.seed, args.out, args.report)
    print({"cache_chaos_rows": len(rows), "out": args.out})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

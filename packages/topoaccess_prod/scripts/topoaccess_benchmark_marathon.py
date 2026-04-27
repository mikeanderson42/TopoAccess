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

from topoaccess_prod.harness.benchmark_marathon import run_marathon


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="demo")
    parser.add_argument("--rows", type=int, default=1000)
    parser.add_argument("--fallback-rows", type=int, default=1000)
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--modes", nargs="+")
    parser.add_argument("--categories", nargs="+")
    parser.add_argument("--out", default="runs/topoaccess_prod_v44/benchmark_marathon.jsonl")
    parser.add_argument("--chunk-dir", default="")
    parser.add_argument("--summary", default="runs/topoaccess_prod_v44/benchmark_summary.json")
    parser.add_argument("--report", default="REPORT_topoaccess_prod_v44_benchmarks.md")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    rows = run_marathon(
        profile=args.profile,
        rows=args.rows,
        fallback_rows=args.fallback_rows,
        chunk_size=args.chunk_size,
        seed=args.seed,
        modes=args.modes,
        categories=args.categories,
        out=args.out,
        chunk_dir=args.chunk_dir or None,
        summary=args.summary,
        report=args.report,
        resume=args.resume,
    )
    print({"benchmark_rows": len(rows), "out": args.out})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

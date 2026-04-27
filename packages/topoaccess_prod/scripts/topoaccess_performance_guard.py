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

from topoaccess_prod.harness.performance_guard import run_performance_guard


def main() -> int:
    parser = argparse.ArgumentParser(description="Check common TopoAccess command latency against public thresholds.")
    parser.add_argument("--profile", default="demo")
    parser.add_argument("--baseline", default="")
    parser.add_argument("--out", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    rows = run_performance_guard(args.profile, args.baseline, args.out, args.report)
    print({"performance_rows": len(rows), "out": args.out})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

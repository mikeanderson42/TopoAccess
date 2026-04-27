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

from topoaccess_prod.harness.regression_matrix import run_regression_matrix


def main() -> int:
    parser = argparse.ArgumentParser(description="Run TopoAccess CLI and legacy-wrapper regression matrix.")
    parser.add_argument("--profile", default="demo")
    parser.add_argument("--out", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    rows = run_regression_matrix(args.profile, args.out, args.report)
    print({"regression_rows": len(rows), "out": args.out})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

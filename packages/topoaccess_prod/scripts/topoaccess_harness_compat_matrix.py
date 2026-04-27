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

from topoaccess_prod.harness.harness_compat_matrix import build_matrix


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default")
    parser.add_argument("--out", default="runs/topoaccess_prod_v37/compat_matrix.jsonl")
    parser.add_argument("--report", default="REPORT_topoaccess_prod_v37_compatibility.md")
    args = parser.parse_args()
    rows = build_matrix(args.profile, args.out, args.report)
    print({"compat_matrix_rows": len(rows)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


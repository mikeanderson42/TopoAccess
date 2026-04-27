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

from topoaccess_prod.integrations.aider_repomap import export_repomap


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default")
    parser.add_argument("--budgets", nargs="+", type=int, default=[1000, 2000, 4000])
    parser.add_argument("--out", default="release/topoaccess_prod_v37/repomap")
    parser.add_argument("--report", default="REPORT_topoaccess_prod_v37_repomap.md")
    args = parser.parse_args()
    rows = export_repomap(args.profile, args.budgets, args.out, args.report)
    print({"repomap_rows": len(rows), "budgets": args.budgets})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


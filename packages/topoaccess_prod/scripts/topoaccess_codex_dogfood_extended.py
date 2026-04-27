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

from topoaccess_prod.harness.codex_dogfood_extended import run_codex_dogfood_extended


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default")
    parser.add_argument("--tasks", type=int, default=250)
    parser.add_argument("--fallback-tasks", type=int, default=100)
    parser.add_argument("--fixture-edits", action="store_true")
    parser.add_argument("--out", default="runs/topoaccess_prod_v37/codex_dogfood_extended.jsonl")
    parser.add_argument("--report", default="REPORT_topoaccess_prod_v37_codex_dogfood.md")
    args = parser.parse_args()
    rows = run_codex_dogfood_extended(args.profile, args.tasks, args.fallback_tasks, args.fixture_edits, args.out, args.report)
    avg = sum(row["codex_savings"] for row in rows) / len(rows)
    print({"codex_dogfood_rows": len(rows), "average_savings": round(avg, 4)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


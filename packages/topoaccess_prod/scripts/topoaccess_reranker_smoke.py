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

from topoaccess_prod.integrations.reranker_adapter import reranker_smoke


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default")
    parser.add_argument("--mode", nargs="+", default=["none", "lexical"])
    parser.add_argument("--out", default="runs/topoaccess_prod_v37/reranker_smoke.jsonl")
    parser.add_argument("--report", default="REPORT_topoaccess_prod_v37_reranker.md")
    args = parser.parse_args()
    rows = reranker_smoke(args.profile, args.mode, args.out, args.report)
    print({"reranker_rows": len(rows), "modes": args.mode})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


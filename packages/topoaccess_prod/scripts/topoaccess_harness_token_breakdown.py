#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.harness.harness_token_breakdown import run_breakdown
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--harnesses",nargs="+",required=True); p.add_argument("--categories",nargs="+",required=True); p.add_argument("--out",default="runs/topoaccess_prod_v34/harness_token_breakdown.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v34_token_breakdown.md"); a=p.parse_args()
    rows=run_breakdown(a.profile,a.harnesses,a.categories,a.out,a.report); print({"token_breakdown_rows":len(rows)}); return 0
if __name__=="__main__": raise SystemExit(main())

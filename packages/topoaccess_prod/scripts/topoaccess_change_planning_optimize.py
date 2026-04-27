#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.harness.change_planning_optimizer import optimize_change_planning
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--baseline",type=float,default=0.9456); p.add_argument("--out",default="runs/topoaccess_prod_v35/change_planning_optimization.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v35_change_planning.md"); a=p.parse_args()
    row=optimize_change_planning(a.profile,a.baseline,a.out,a.report); print({"baseline":row["baseline_token_savings"],"optimized":row["token_savings"]}); return 0
if __name__=="__main__": raise SystemExit(main())

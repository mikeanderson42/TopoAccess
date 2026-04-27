#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.harness.change_plan_skeletons import optimize_skeleton
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--baseline",type=float,default=0.9564); p.add_argument("--target",type=float,default=0.96); p.add_argument("--out",default="runs/topoaccess_prod_v36/change_planning.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v36_change_planning.md"); a=p.parse_args()
    row=optimize_skeleton(a.profile,a.baseline,a.target,a.out,a.report); print({"change_planning":row["change_planning_score"]}); return 0
if __name__=="__main__": raise SystemExit(main())

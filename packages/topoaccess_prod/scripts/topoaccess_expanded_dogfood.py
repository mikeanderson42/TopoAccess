#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.harness.expanded_dogfood import run_expanded_dogfood
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--tasks",type=int,default=100); p.add_argument("--fallback-tasks",type=int,default=50); p.add_argument("--out",default="runs/topoaccess_prod_v35/expanded_dogfood.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v35_dogfood.md"); a=p.parse_args()
    rows=run_expanded_dogfood(a.profile,a.tasks,a.fallback_tasks,a.out,a.report); print({"expanded_dogfood_rows":len(rows)}); return 0
if __name__=="__main__": raise SystemExit(main())

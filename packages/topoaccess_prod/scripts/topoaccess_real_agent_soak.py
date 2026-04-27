#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.harness.real_agent_soak import run_soak
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--tasks",type=int,default=5000); p.add_argument("--fallback-tasks",type=int,default=1000); p.add_argument("--modes",nargs="+",required=True); p.add_argument("--out",default="runs/topoaccess_prod_v32/real_agent_soak.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v32_real_agent_soak.md"); a=p.parse_args()
    rows=run_soak(a.tasks,a.fallback_tasks,a.modes,a.out,a.report); print({"real_agent_soak_rows":len(rows)}); return 0
if __name__=="__main__": raise SystemExit(main())

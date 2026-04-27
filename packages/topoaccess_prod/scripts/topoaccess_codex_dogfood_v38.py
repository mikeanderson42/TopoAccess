#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.harness.codex_dogfood_v38 import run_codex_dogfood_v38
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--tasks",type=int,default=500); p.add_argument("--fallback-tasks",type=int,default=250); p.add_argument("--fixture-edits",action="store_true"); p.add_argument("--out",default="runs/topoaccess_prod_v38/codex_dogfood.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v38_codex_dogfood.md"); a=p.parse_args()
    rows=run_codex_dogfood_v38(a.profile,a.tasks,a.fallback_tasks,a.fixture_edits,a.out,a.report); avg=sum(r["codex_savings"] for r in rows)/len(rows); print({"codex_rows":len(rows),"average_savings":round(avg,4)}); return 0
if __name__=="__main__": raise SystemExit(main())


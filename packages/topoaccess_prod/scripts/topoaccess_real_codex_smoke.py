#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.harness.real_codex_smoke import run_real_codex_smoke
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--tasks",type=int,default=25); p.add_argument("--read-only",action="store_true"); p.add_argument("--out",default="runs/topoaccess_prod_v35/real_codex_smoke.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v35_dogfood.md"); a=p.parse_args()
    rows=run_real_codex_smoke(a.profile,a.tasks,a.read_only,a.out,a.report); print({"real_codex_smoke_rows":len(rows),"detected":rows[0]["codex_detected"] if rows else False}); return 0
if __name__=="__main__": raise SystemExit(main())

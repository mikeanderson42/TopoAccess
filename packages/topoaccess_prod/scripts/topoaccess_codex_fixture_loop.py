#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.harness.codex_fixture_loop import run_codex_fixture_loop
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--read-only-tasks",type=int,default=100); p.add_argument("--fallback-read-only-tasks",type=int,default=50); p.add_argument("--fixture-tasks",type=int,default=25); p.add_argument("--out",default="runs/topoaccess_prod_v36/codex_fixture_loop.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v36_codex_dogfood.md"); a=p.parse_args()
    rows=run_codex_fixture_loop(a.profile,a.read_only_tasks,a.fallback_read_only_tasks,a.fixture_tasks,a.out,a.report); print({"codex_fixture_rows":len(rows)}); return 0
if __name__=="__main__": raise SystemExit(main())

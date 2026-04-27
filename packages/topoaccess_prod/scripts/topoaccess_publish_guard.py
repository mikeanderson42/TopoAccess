#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.harness.publish_guard import run_publish_guard
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--branch",default="topoaccess-prod-v33-publish"); p.add_argument("--release",default="release/topoaccess_prod_v33"); p.add_argument("--out",default="runs/topoaccess_prod_v34/publish_guard.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v34_publish_guard.md"); a=p.parse_args()
    row=run_publish_guard(a.branch,a.release,a.out,a.report); print({"publish_guard":row["result_status"],"push_allowed":row["push_allowed"]}); return 0 if row["result_status"]=="pass" else 1
if __name__=="__main__": raise SystemExit(main())

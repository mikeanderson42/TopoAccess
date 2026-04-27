#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.safe_publish import safe_publish
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--branch",required=True); p.add_argument("--release",required=True); p.add_argument("--dry-run",action="store_true"); p.add_argument("--out",default="runs/topoaccess_prod_v36/safe_publish.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v36_publish.md"); a=p.parse_args()
    row=safe_publish(a.branch,a.release,a.dry_run,a.out,a.report); print({"safe_publish":row["result_status"],"publish_ready":row["publish_ready"],"remote_configured":row["remote_configured"]}); return 0 if row["result_status"]=="pass" else 1
if __name__=="__main__": raise SystemExit(main())

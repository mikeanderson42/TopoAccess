#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.safe_sync_wrapper import safe_sync
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--branch",default="topoaccess-prod-v38-distribution"); p.add_argument("--release",default="release/topoaccess_prod_v38"); p.add_argument("--candidate-sync",action="append",default=[]); p.add_argument("--dry-run",action="store_true"); p.add_argument("--out",default="runs/topoaccess_prod_v38/safe_sync.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v38_safe_sync.md"); a=p.parse_args()
    row=safe_sync(a.branch,a.release,a.candidate_sync,a.dry_run,a.out,a.report); print({"safe_sync":row["result_status"],"remote_configured":row["remote_configured"],"unsafe_sync_used":row["unsafe_sync_used"]}); return 0
if __name__=="__main__": raise SystemExit(main())


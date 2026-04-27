#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.sync_script_guard import inspect_sync_script
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--candidate",action="append",default=[]); p.add_argument("--branch",default="topoaccess-prod-v33-publish"); p.add_argument("--dry-run-only",action="store_true"); p.add_argument("--out",default="runs/topoaccess_prod_v35/sync_guard.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v35_sync.md"); a=p.parse_args()
    row=inspect_sync_script(a.candidate,a.branch,a.dry_run_only,a.out,a.report); print({"sync_script_found":row["sync_script_found"],"sync_script_safe_dry_run":row["sync_script_safe_dry_run"]}); return 0
if __name__=="__main__": raise SystemExit(main())

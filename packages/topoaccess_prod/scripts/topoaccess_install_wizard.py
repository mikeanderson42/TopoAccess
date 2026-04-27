#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.install.install_wizard import run_install_wizard
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--repo",default="."); p.add_argument("--cache",default="cache/topoaccess_v21"); p.add_argument("--preferred-search",default="runs/topoaccess_v22/preferred_model_search.jsonl"); p.add_argument("--dry-run",action="store_true"); p.add_argument("--out",default="runs/topoaccess_prod_v35/install_wizard.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v35_install.md"); a=p.parse_args()
    row=run_install_wizard(a.profile,a.repo,a.cache,a.preferred_search,a.dry_run,a.out,a.report); print({"install_wizard":row["result_status"]}); return 0
if __name__=="__main__": raise SystemExit(main())

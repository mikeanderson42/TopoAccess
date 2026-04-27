#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.install.editable_install import editable_install_smoke
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package",default="packages/topoaccess_prod"); p.add_argument("--dry-run-first",action="store_true"); p.add_argument("--out",default="runs/topoaccess_prod_v36/editable_install.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v36_distribution.md"); a=p.parse_args()
    row=editable_install_smoke(a.package,a.dry_run_first,a.out,a.report); print({"editable_install":row["result_status"],"installed":row["installed"]}); return 0 if row["result_status"]=="pass" else 1
if __name__=="__main__": raise SystemExit(main())

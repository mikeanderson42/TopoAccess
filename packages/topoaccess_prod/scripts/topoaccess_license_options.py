#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.license_options import write_license_options
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package",default="packages/topoaccess_prod"); p.add_argument("--out",default="runs/topoaccess_prod_v35/license_options.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v35_license.md"); a=p.parse_args()
    rows=write_license_options(a.package,a.out,a.report); print({"license_options":len(rows),"license_confirmed":rows[0]["license_confirmed"]}); return 0
if __name__=="__main__": raise SystemExit(main())

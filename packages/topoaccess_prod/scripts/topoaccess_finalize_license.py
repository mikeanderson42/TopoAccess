#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.license_finalize import finalize_license
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package",default="packages/topoaccess_prod"); p.add_argument("--license",default="apache-2.0"); p.add_argument("--creator",default="Mike"); p.add_argument("--out",default="runs/topoaccess_prod_v36/license_finalize.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v36_license.md"); a=p.parse_args()
    row=finalize_license(a.package,a.license,a.creator,a.out,a.report); print({"license":row["license"],"license_confirmed":row["license_confirmed"]}); return 0
if __name__=="__main__": raise SystemExit(main())

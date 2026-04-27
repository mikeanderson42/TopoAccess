#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.distribution_builder import build_distribution
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package",default="packages/topoaccess_prod"); p.add_argument("--out",default="release/topoaccess_prod_v38/dist"); p.add_argument("--report",default="REPORT_topoaccess_prod_v38_distribution.md"); a=p.parse_args()
    rows=build_distribution(a.package,a.out,a.report); print({"dist_rows":len(rows),"artifact":rows[-1]["build_artifact"]}); return 0
if __name__=="__main__": raise SystemExit(main())


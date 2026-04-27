#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.dist_smoke import dist_smoke
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package",default="packages/topoaccess_prod"); p.add_argument("--out",default="runs/topoaccess_prod_v36/dist_smoke.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v36_distribution.md"); a=p.parse_args()
    row=dist_smoke(a.package,a.out,a.report); print({"dist_smoke":row["result_status"]}); return 0 if row["result_status"]=="pass" else 1
if __name__=="__main__": raise SystemExit(main())

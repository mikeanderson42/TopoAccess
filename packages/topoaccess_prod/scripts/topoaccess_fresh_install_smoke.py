#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.fresh_install import run_fresh_install_smoke
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package",default="packages/topoaccess_prod"); p.add_argument("--dist",default="release/topoaccess_prod_v38/dist"); p.add_argument("--out",default="runs/topoaccess_prod_v38/fresh_install.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v38_distribution.md"); a=p.parse_args()
    rows=run_fresh_install_smoke(a.package,a.dist,a.out,a.report); print({"fresh_install_rows":len(rows),"statuses":[r["install_status"] for r in rows]}); return 0
if __name__=="__main__": raise SystemExit(main())


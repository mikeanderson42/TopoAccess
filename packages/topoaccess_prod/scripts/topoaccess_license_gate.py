#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.harness.license_gate import run_license_gate
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package",default="packages/topoaccess_prod"); p.add_argument("--out",default="runs/topoaccess_prod_v34/license_gate.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v34_license_gate.md"); a=p.parse_args()
    row=run_license_gate(a.package,a.out,a.report); print({"license_confirmed":row["license_confirmed"],"public_publish_ready":row["public_publish_ready"]}); return 0
if __name__=="__main__": raise SystemExit(main())

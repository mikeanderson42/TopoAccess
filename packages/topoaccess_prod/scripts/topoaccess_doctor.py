#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.install.doctor import write_doctor
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--out",default="runs/topoaccess_prod_v32/doctor.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v32_installers.md"); a=p.parse_args()
    rows=write_doctor(a.profile,a.out,a.report); print({"doctor_rows":len(rows)}); return 0
if __name__=="__main__": raise SystemExit(main())

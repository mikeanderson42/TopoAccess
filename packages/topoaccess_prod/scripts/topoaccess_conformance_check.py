#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.conformance import check_conformance
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--release",default="release/topoaccess_prod_v37"); p.add_argument("--out",default="runs/topoaccess_prod_v38/conformance.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v38_conformance.md"); a=p.parse_args()
    rows=check_conformance(a.release,a.out,a.report); failures=[r for r in rows if r["result_status"]!="pass"]; print({"conformance_rows":len(rows),"failures":len(failures)}); return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())


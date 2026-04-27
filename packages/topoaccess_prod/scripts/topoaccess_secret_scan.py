#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.secret_scan import scan_secrets
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--paths",nargs="+",required=True); p.add_argument("--out",default="runs/topoaccess_prod_v35/secret_scan.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v35_security.md"); a=p.parse_args()
    rows=scan_secrets(a.paths,a.out,a.report); fails=sum(r["result_status"]=="fail" for r in rows); print({"secret_scan_files":len(rows),"failures":fails}); return 0 if fails==0 else 1
if __name__=="__main__": raise SystemExit(main())

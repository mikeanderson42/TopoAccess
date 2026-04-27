#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.harness.external_client_probe import probe_clients
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--out",default="runs/topoaccess_prod_v34/external_client_probe.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v34_external_clients.md"); a=p.parse_args()
    rows=probe_clients(a.out,a.report); print({"external_probe_rows":len(rows)}); return 0
if __name__=="__main__": raise SystemExit(main())

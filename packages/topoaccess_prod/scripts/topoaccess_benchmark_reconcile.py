#!/usr/bin/env python
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.harness.benchmark_reconciler import reconcile
if __name__=="__main__":
    rows=reconcile("runs/topoaccess_prod_v32/benchmark_reconcile.jsonl","REPORT_topoaccess_prod_v32_candidate.md")
    print({"benchmark_reconcile_rows":len(rows)})

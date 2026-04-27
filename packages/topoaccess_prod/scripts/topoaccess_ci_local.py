#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.ci_templates import write_ci_templates
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package",default="packages/topoaccess_prod"); p.add_argument("--out",default="runs/topoaccess_prod_v38/ci_local.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v38_ci.md"); a=p.parse_args()
    rows=write_ci_templates(a.package,a.out,a.report); print({"ci_status":rows[-1]["ci_status"],"github_actions_generated":rows[-1]["github_actions_generated"]}); return 0 if rows[-1]["ci_status"]=="pass" else 1
if __name__=="__main__": raise SystemExit(main())


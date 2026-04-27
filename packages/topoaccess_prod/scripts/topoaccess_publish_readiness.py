#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.publish_readiness import publish_readiness
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package",default="packages/topoaccess_prod"); p.add_argument("--release",default="release/topoaccess_prod_v34"); p.add_argument("--branch",default="topoaccess-prod-v33-publish"); p.add_argument("--out",default="runs/topoaccess_prod_v35/publish_readiness.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v35_release.md"); a=p.parse_args()
    row=publish_readiness(a.package,a.release,a.branch,a.out,a.report); print({"public_publish_ready":row["public_publish_ready"],"local_release_ready":row["local_release_ready"]}); return 0
if __name__=="__main__": raise SystemExit(main())

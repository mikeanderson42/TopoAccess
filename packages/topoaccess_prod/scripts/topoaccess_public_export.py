#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.public_export import public_export
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--source",default="."); p.add_argument("--target",default="build/topoaccess_public_repo"); p.add_argument("--layout",default="root-package-preferred"); p.add_argument("--out",default="runs/topoaccess_prod_v39/public_export.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v39_repo_layout.md"); a=p.parse_args()
    row=public_export(a.source,a.target,a.layout,a.out,a.report); print({"public_export_path":row["public_export_path"],"files_copied":row["files_copied"],"layout":row["public_layout_mode"]}); return 0
if __name__=="__main__": raise SystemExit(main())


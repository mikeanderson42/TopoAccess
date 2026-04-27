#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.install.harness_installer import write_installers
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--target",required=True); p.add_argument("--profile",default="default"); p.add_argument("--dry-run",action="store_true"); p.add_argument("--out",default="runs/topoaccess_prod_v32/installers.jsonl"); a=p.parse_args()
    rows=write_installers([a.target],a.profile,True,a.out); print({"installer_rows":len(rows)}); return 0
if __name__=="__main__": raise SystemExit(main())

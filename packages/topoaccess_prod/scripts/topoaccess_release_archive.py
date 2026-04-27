#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.release.release_archive import build_release_archive
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--package",default="packages/topoaccess_prod"); p.add_argument("--release",default="release/topoaccess_prod_v38"); p.add_argument("--out",default="runs/topoaccess_prod_v38/release_archive.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v38_release.md"); a=p.parse_args()
    row=build_release_archive(a.package,a.release,a.out,a.report); print({"archive":row["build_artifact"],"bytes":row["archive_bytes"]}); return 0
if __name__=="__main__": raise SystemExit(main())


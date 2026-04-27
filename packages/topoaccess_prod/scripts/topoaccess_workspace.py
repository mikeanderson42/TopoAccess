#!/usr/bin/env python
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.install.workspace_init import detect_workspace, init_workspace, list_workspaces, validate_workspace
def main() -> int:
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    i=sub.add_parser("init"); i.add_argument("--profile",default="default"); i.add_argument("--repo",default="."); i.add_argument("--cache",default=".topoaccess/cache"); i.add_argument("--preferred-search",default=".topoaccess/preferred_model_search.jsonl")
    d=sub.add_parser("detect"); d.add_argument("--repo",default=".")
    sub.add_parser("list")
    s=sub.add_parser("status"); s.add_argument("--profile",default="default")
    v=sub.add_parser("validate"); v.add_argument("--profile",default="default")
    a=p.parse_args()
    result={"init":lambda:init_workspace(a.profile,a.repo,a.cache,a.preferred_search),"detect":lambda:detect_workspace(a.repo),"list":list_workspaces,"status":lambda:validate_workspace(a.profile),"validate":lambda:validate_workspace(a.profile)}[a.cmd]()
    print(json.dumps(result,indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())

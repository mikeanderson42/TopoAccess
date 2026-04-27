#!/usr/bin/env python
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--cache",default="cache/topoaccess_v21"); p.add_argument("--release",default="release/topoaccess_prod_v39"); p.add_argument("--remote",default="https://github.com/mikeanderson42/TopoAccess.git"); p.add_argument("--resume",action="store_true"); p.add_argument("--heartbeat-seconds",type=int,default=30); a=p.parse_args()
    steps=[
        ["python","packages/topoaccess_prod/scripts/topoaccess_public_export.py","--source",".","--target","build/topoaccess_public_repo","--layout","root-package-preferred"],
        ["python","-m","compileall","build/topoaccess_public_repo"],
    ]
    rows=[]
    for step in steps:
        proc=subprocess.run(step,text=True,capture_output=True,timeout=180)
        rows.append({"command":" ".join(step),"returncode":proc.returncode,"result_status":"pass" if proc.returncode==0 else "fail"})
    out=Path("runs/topoaccess_prod_v39/autopilot.jsonl"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text("\\n".join(json.dumps(r,sort_keys=True) for r in rows)+"\\n",encoding="utf-8")
    failures=[r for r in rows if r["returncode"]!=0]; print({"autopilot_rows":len(rows),"failures":len(failures),"release":a.release}); return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())


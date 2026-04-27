#!/usr/bin/env python
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

STEPS = [
    ["python","packages/topoaccess_prod/scripts/topoaccess_build_dist.py","--package","packages/topoaccess_prod","--out","release/topoaccess_prod_v38/dist"],
    ["python","packages/topoaccess_prod/scripts/topoaccess_fresh_install_smoke.py","--package","packages/topoaccess_prod","--dist","release/topoaccess_prod_v38/dist"],
    ["python","packages/topoaccess_prod/scripts/topoaccess_ci_local.py","--package","packages/topoaccess_prod"],
    ["python","packages/topoaccess_prod/scripts/topoaccess_safe_sync.py","--branch","topoaccess-prod-v38-distribution","--release","release/topoaccess_prod_v38","--candidate-sync","<local-sync-script-path>","--dry-run"],
    ["python","packages/topoaccess_prod/scripts/topoaccess_conformance_check.py","--release","release/topoaccess_prod_v37"],
    ["python","packages/topoaccess_prod/scripts/topoaccess_codex_dogfood_v38.py","--profile","default","--tasks","500","--fallback-tasks","250","--fixture-edits"],
    ["python","packages/topoaccess_prod/scripts/topoaccess_status_badges.py","--release","release/topoaccess_prod_v38"],
    ["python","packages/topoaccess_prod/scripts/topoaccess_release_archive.py","--package","packages/topoaccess_prod","--release","release/topoaccess_prod_v38"],
]

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--cache",default="cache/topoaccess_v21"); p.add_argument("--release",default="release/topoaccess_prod_v38"); p.add_argument("--resume",action="store_true"); p.add_argument("--heartbeat-seconds",type=int,default=30); a=p.parse_args()
    rows=[]
    for step in STEPS:
        proc=subprocess.run(step,text=True,capture_output=True,timeout=240)
        rows.append({"command":" ".join(step),"returncode":proc.returncode,"result_status":"pass" if proc.returncode==0 else "fail"})
    out=Path("runs/topoaccess_prod_v38/autopilot.jsonl"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text("\\n".join(json.dumps(r,sort_keys=True) for r in rows)+"\\n",encoding="utf-8")
    failures=[r for r in rows if r["returncode"]!=0]; print({"autopilot_rows":len(rows),"failures":len(failures),"release":a.release}); return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())


#!/usr/bin/env python
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
for path in [ROOT, REPO]:
    if str(path) not in sys.path: sys.path.insert(0, str(path))
from topoaccess_prod.harness.token_accounting import run_token_accounting
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--profile",default="default"); p.add_argument("--tasks",nargs="+",required=True); p.add_argument("--out",default="runs/topoaccess_prod_v31/token_accounting.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v31_token_accounting.md"); a=p.parse_args()
    rows=run_token_accounting(a.tasks,a.out)
    avg=sum(r["token_savings"] for r in rows)/len(rows)
    Path(a.report).write_text(f"# Token Accounting\n\nAverage token savings vs direct preferred-model baseline: `{avg:.4f}`.\n",encoding="utf-8")
    print({"token_accounting_rows":len(rows),"average_token_savings":round(avg,4)})
    return 0
if __name__=="__main__": raise SystemExit(main())

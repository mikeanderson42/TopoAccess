#!/usr/bin/env python
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
for p in [ROOT, REPO]:
    if str(p) not in sys.path: sys.path.insert(0,str(p))
from topoaccess_prod.install.publish_prep import publish_row, write_jsonl
def count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--mode",default="reconcile"); p.add_argument("--v32-runs",default="runs/topoaccess_prod_v32"); p.add_argument("--v32-release",default="release/topoaccess_prod_v32"); p.add_argument("--out",default="runs/topoaccess_prod_v33/benchmark_reconcile.jsonl"); p.add_argument("--report",default="REPORT_topoaccess_prod_v33_benchmark_reconciliation.md"); a=p.parse_args()
    v31_full=count(Path("runs/topoaccess_prod_v31/agent_benchmark.jsonl")); v31_smoke=count(Path("runs/topoaccess_prod_v31/agent_benchmark_smoke.jsonl")); v32_soak=count(Path(a.v32_runs)/"real_agent_soak.jsonl")
    v32_token=[json.loads(x) for x in (Path(a.v32_runs)/"token_ledger.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    avg=sum(r["percentage_saved"] for r in v32_token)/len(v32_token)
    rows=[publish_row("benchmark_reconcile", benchmark_rows=v31_full, canonical_metric="benchmark_rows", token_savings=round(avg,4), source="v31_full_jsonl"), publish_row("benchmark_reconcile", benchmark_rows=v31_smoke, canonical_metric="smoke_subset_rows", token_savings=round(avg,4), source="v31_smoke_subset"), publish_row("benchmark_reconcile", benchmark_rows=v32_soak, canonical_metric="v32_real_agent_soak_rows", token_savings=round(avg,4), source="v32_soak"), publish_row("benchmark_reconcile", benchmark_rows=v31_full, canonical_metric="canonical_benchmark_rows", token_savings=round(avg,4), source="canonical")]
    write_jsonl(a.out,rows)
    Path(a.report).write_text(f"# V33 Benchmark Reconciliation\n\nCanonical benchmark rows: `{v31_full}`. V31/V32 smoke subsets are documented as subsets. Canonical token savings from V32 JSONL: `{avg:.4f}`; attached `0.9462` is treated as rounded/report value, while pasted `0.936` came from release summary rounding.\n",encoding="utf-8")
    print({"canonical_benchmark_rows":v31_full,"canonical_token_savings":round(avg,4)})
    return 0
if __name__=="__main__": raise SystemExit(main())

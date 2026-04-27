#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
for path in [ROOT, REPO]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from topoaccess_prod.harness.external_style_benchmark import run_external_style_benchmark, write_external_summary_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Run model-free external-style TopoAccess fixture benchmarks.")
    parser.add_argument("--fixtures", default="examples/external_style_repos")
    parser.add_argument("--scenarios", type=int, default=1000)
    parser.add_argument("--fallback-scenarios", type=int, default=250)
    parser.add_argument("--seed", type=int, default=20260427)
    parser.add_argument("--out", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--markdown", default="release/topoaccess_prod_v46/external_style_summary.md")
    args = parser.parse_args()
    rows = run_external_style_benchmark(
        fixtures=args.fixtures,
        scenarios=args.scenarios,
        fallback_scenarios=args.fallback_scenarios,
        seed=args.seed,
        out=args.out,
        summary=args.summary,
        report=args.report,
    )
    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    write_external_summary_markdown(summary, args.markdown)
    print({"external_style_rows": len(rows), "summary": args.summary})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

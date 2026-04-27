#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
for path in [ROOT, REPO]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from topoaccess_prod.harness.benchmark_stats import load_rows, write_summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--markdown", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    rows = load_rows(args.input)
    summary = write_summary(rows, args.out, args.markdown)
    Path(args.report).write_text(
        "# TopoAccess Benchmark Summary\n\n"
        f"- Rows: `{summary['rows']}`\n"
        f"- Average assisted token savings: `{summary['average_token_savings']:.4f}`\n"
        f"- Median assisted token savings: `{summary['median_token_savings']:.4f}`\n"
        f"- p50/p95 latency: `{summary['p50_latency_ms']:.1f} ms` / `{summary['p95_latency_ms']:.1f} ms`\n",
        encoding="utf-8",
    )
    print({"rows": summary["rows"], "average_token_savings": summary["average_token_savings"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

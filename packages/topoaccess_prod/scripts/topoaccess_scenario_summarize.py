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

from topoaccess_prod.harness.scenario_benchmark import _load_rows, write_scenario_markdown, write_scenario_summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--markdown", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    rows = _load_rows(Path(args.input))
    summary = write_scenario_summary(rows, args.out, args.report)
    write_scenario_markdown(summary, args.markdown)
    print({"scenario_steps": summary["steps"], "average_token_savings": summary["average_token_savings"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

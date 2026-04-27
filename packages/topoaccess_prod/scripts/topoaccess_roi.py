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

from topoaccess_prod.harness.roi_calculator import estimate_roi, scenario_table


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate token and optional cost savings from TopoAccess.")
    parser.add_argument("--tasks-per-day", type=int, default=100)
    parser.add_argument("--tokens-per-task", type=int, default=20_000)
    parser.add_argument("--savings", type=float, default=0.9307)
    parser.add_argument("--price-per-million-tokens", type=float, default=0.0)
    parser.add_argument("--table", action="store_true")
    args = parser.parse_args()
    data = scenario_table(args.tokens_per_task, args.price_per_million_tokens) if args.table else estimate_roi(
        args.tasks_per_day,
        args.tokens_per_task,
        args.savings,
        args.price_per_million_tokens,
    )
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

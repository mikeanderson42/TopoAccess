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

from topoaccess_prod.harness.fixture_mutator import run_fixture_mutations


def main() -> int:
    parser = argparse.ArgumentParser(description="Run mutation-style checks over public fixture repositories.")
    parser.add_argument("--fixtures", nargs="+", default=["examples/scenario_repos"])
    parser.add_argument("--mutations", type=int, default=250)
    parser.add_argument("--fallback-mutations", type=int, default=250)
    parser.add_argument("--seed", type=int, default=4604)
    parser.add_argument("--out", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    rows = run_fixture_mutations(args.fixtures, args.mutations, args.fallback_mutations, args.seed, args.out, args.report)
    print({"fixture_mutation_rows": len(rows), "out": args.out})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

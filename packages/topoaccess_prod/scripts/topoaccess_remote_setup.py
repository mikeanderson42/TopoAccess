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

from topoaccess_prod.release.remote_setup import remote_setup


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", default="topoaccess-prod-v36-release")
    parser.add_argument("--release", default="release/topoaccess_prod_v36")
    parser.add_argument("--out", default="runs/topoaccess_prod_v37/remote_setup.jsonl")
    parser.add_argument("--report", default="REPORT_topoaccess_prod_v37_publish.md")
    args = parser.parse_args()
    row = remote_setup(args.branch, args.release, args.out, args.report)
    print({"remote_configured": row["remote_configured"], "result_status": row["result_status"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


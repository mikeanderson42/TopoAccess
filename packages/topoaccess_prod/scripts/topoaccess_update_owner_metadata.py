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

from topoaccess_prod.release.owner_metadata import update_owner_metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", default="packages/topoaccess_prod")
    parser.add_argument("--creator", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--out", default="runs/topoaccess_prod_v37/metadata.jsonl")
    parser.add_argument("--report", default="REPORT_topoaccess_prod_v37_metadata.md")
    args = parser.parse_args()
    row = update_owner_metadata(args.package, args.creator, args.email, args.out, args.report)
    print({"metadata_owner": row["metadata_owner"], "result_status": row["result_status"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


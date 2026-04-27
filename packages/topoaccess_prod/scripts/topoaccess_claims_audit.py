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

from topoaccess_prod.harness.claims_audit import claims_gate_passed, write_claims_audit


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit public markdown claims for unsupported absolute wording.")
    parser.add_argument("--paths", nargs="+", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    rows = write_claims_audit(args.paths, args.out, args.report)
    failures = 0 if claims_gate_passed(rows) else sum(1 for row in rows if row["result_status"] != "pass")
    print({"claims_reviewed": len(rows), "failures": failures})
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

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

from topoaccess_prod.harness.robustness_report import write_robustness_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize V47 robustness outputs into compact release assets.")
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--markdown", required=True)
    parser.add_argument("--failures", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()
    summary = write_robustness_summary(args.inputs, args.out, args.markdown, args.failures, args.manifest)
    print({"robustness_rows": summary.get("rows", 0), "failures": summary.get("failures", 0)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

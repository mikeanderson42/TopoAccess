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

from topoaccess_prod.integrations.cursor_rules import generate_cursor_rules


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--out", default="release/topoaccess_prod_v37/cursor_rules")
    parser.add_argument("--report", default="REPORT_topoaccess_prod_v37_agent_configs.md")
    args = parser.parse_args()
    row = generate_cursor_rules(args.profile, args.out, args.report)
    print({"generated_file": row["generated_file"], "dry_run": args.dry_run})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


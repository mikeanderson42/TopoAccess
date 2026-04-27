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

from topoaccess_prod.integrations.http_tool_server import serve


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--profile", default="default")
    p.add_argument("--port", type=int, default=8876)
    p.add_argument("--smoke", action="store_true")
    args = p.parse_args()
    if args.smoke:
        print({"http_tool_server": "ready", "port": args.port, "profile": args.profile})
        return 0
    serve(args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

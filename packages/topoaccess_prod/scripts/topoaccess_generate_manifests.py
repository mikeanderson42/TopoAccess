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

from topoaccess_prod.integrations.mcp_manifest import mcp_manifest, stdio_schema
from topoaccess_prod.integrations.openapi_manifest import openapi_manifest
from topoaccess_prod.integrations.tool_schema import write_tool_schema
from topoaccess_prod.integrations.agents_md import base_row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default")
    parser.add_argument("--out", default="release/topoaccess_prod_v37")
    parser.add_argument("--report", default="REPORT_topoaccess_prod_v37_compatibility.md")
    args = parser.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    tool_schema = write_tool_schema(out_dir / "tool_schema.json")
    (out_dir / "openapi.json").write_text(json.dumps(openapi_manifest(), indent=2, sort_keys=True), encoding="utf-8")
    (out_dir / "mcp_like_manifest.json").write_text(json.dumps(mcp_manifest(), indent=2, sort_keys=True), encoding="utf-8")
    (out_dir / "stdio_schema.json").write_text(json.dumps(stdio_schema(), indent=2, sort_keys=True), encoding="utf-8")
    row = base_row("manifests", str(out_dir / "tool_schema.json"))
    row.update({"tool_count": len(tool_schema["tools"]), "profile": args.profile})
    run_path = Path("runs/topoaccess_prod_v37/manifests.jsonl")
    run_path.parent.mkdir(parents=True, exist_ok=True)
    run_path.write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.report).write_text(
        "# V37 Tool Manifests\n\nGenerated tool schema, OpenAPI, MCP-like manifest, and stdio schema. Exact lookup forbids model fallback and post-edit validation is read-only.\n",
        encoding="utf-8",
    )
    print({"generated": ["tool_schema.json", "openapi.json", "mcp_like_manifest.json", "stdio_schema.json"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


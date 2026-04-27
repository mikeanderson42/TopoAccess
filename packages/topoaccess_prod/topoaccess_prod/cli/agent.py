from __future__ import annotations

import argparse
import json

from ..harness.benchmark import run_benchmark
from ..harness.post_edit_validation import run_fixture, validate_post_edit
from ..harness.prompt_pack import build_prompt_pack
from ..harness.workspace import detect_workspace, list_profiles, profile_status, write_profiles
from ..integrations.claude_code_adapter import claude_tool_spec
from ..integrations.codex_adapter import codex_brief, codex_post_edit
from ..integrations.generic_agent_adapter import command_recommendation, preflight_query, test_recommendation
from ..integrations.mcp_like_stdio import run_stdio
from ..integrations.openclaw_adapter import openclaw_tool_spec
from ..integrations.tool_schema import write_tool_schema


def run_agent(args: argparse.Namespace) -> dict | None:
    if args.command == "workspace":
        if args.workspace_command == "list":
            write_profiles("runs/topoaccess_prod_v31/workspace_profiles.jsonl")
            return {"profiles": list_profiles()}
        if args.workspace_command == "detect":
            return detect_workspace(args.repo)
        return profile_status(args.profile)
    if args.command == "preflight":
        return preflight_query(args.task, args.profile)
    if args.command == "test-impact":
        return test_recommendation(args.changed_file)
    if args.command == "post-edit":
        return validate_post_edit(args.changed_files)
    if args.command == "codex-brief":
        return codex_brief(args.task, args.profile)
    if args.command == "codex-post-edit":
        return codex_post_edit(args.changed_files)
    if args.command == "claude-spec":
        return claude_tool_spec(args.task)
    if args.command == "openclaw-spec":
        return openclaw_tool_spec(args.task)
    if args.command == "tool-schema":
        return write_tool_schema(args.out)
    if args.command == "prompt-pack":
        return build_prompt_pack(args.task, args.mode)
    if args.command == "post-edit-fixture":
        rows = run_fixture(args.fixture, args.out)
        return {"rows": len(rows), "out": args.out}
    if args.command == "stdio":
        run_stdio()
        return None
    if args.command == "benchmark-smoke":
        rows = run_benchmark(["codex_style_with_topoaccess"], ["exact_lookup"], 1, 1, args.out)
        return {"rows": len(rows), "out": args.out}
    return command_recommendation(args.task)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="topoaccess_agent")
    sub = p.add_subparsers(dest="command", required=True)
    wsp = sub.add_parser("workspace")
    wsp_sub = wsp.add_subparsers(dest="workspace_command", required=True)
    wsp_sub.add_parser("list")
    detect = wsp_sub.add_parser("detect")
    detect.add_argument("--repo", default=".")
    status = wsp_sub.add_parser("status")
    status.add_argument("--profile", default="default")
    for name in ["preflight", "codex-brief", "claude-spec", "openclaw-spec", "prompt-pack"]:
        sp = sub.add_parser(name)
        sp.add_argument("--profile", default="default")
        sp.add_argument("--task", required=True)
        sp.add_argument("--mode", default="standard")
    ti = sub.add_parser("test-impact")
    ti.add_argument("--profile", default="default")
    ti.add_argument("--changed-file", required=True)
    pe = sub.add_parser("post-edit")
    pe.add_argument("--profile", default="default")
    pe.add_argument("--changed-files", nargs="+", required=True)
    cpe = sub.add_parser("codex-post-edit")
    cpe.add_argument("--profile", default="default")
    cpe.add_argument("--changed-files", nargs="+", required=True)
    ts = sub.add_parser("tool-schema")
    ts.add_argument("--out", default="runs/topoaccess_prod_v31/tool_schema.json")
    pef = sub.add_parser("post-edit-fixture")
    pef.add_argument("--profile", default="default")
    pef.add_argument("--fixture", required=True)
    pef.add_argument("--out", default="runs/topoaccess_prod_v31/post_edit_validation.jsonl")
    pef.add_argument("--report", default="")
    stdio = sub.add_parser("stdio")
    bench = sub.add_parser("benchmark-smoke")
    bench.add_argument("--out", default="runs/topoaccess_prod_v31/agent_benchmark_smoke.jsonl")
    args = p.parse_args(argv)
    result = run_agent(args)
    if result is not None:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse

from . import commands
from .command_registry import command_names
from .help_text import DESCRIPTION, EPILOG


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="topoaccess", description=DESCRIPTION, epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("version", help="Print package version and model-free public posture.").set_defaults(handler=commands.cmd_version)
    sub.add_parser("commands", help="List supported commands.").set_defaults(handler=commands.cmd_commands)

    init = sub.add_parser("init", help="Create a demo workspace and local cache for first use.")
    init.add_argument("--profile", default="demo")
    init.add_argument("--repo", default=".")
    init.add_argument("--cache", default=".topoaccess/cache")
    init.set_defaults(handler=commands.cmd_init)

    try_demo = sub.add_parser("try", help="Run a self-contained model-free demo.")
    try_demo.add_argument("--profile", default="demo")
    try_demo.add_argument("--repo", default=".")
    try_demo.set_defaults(handler=commands.cmd_try)

    workspace = sub.add_parser("workspace", help="Manage workspace profiles.")
    wsp = workspace.add_subparsers(dest="workspace_command", required=True)
    init = wsp.add_parser("init", help="Create a fresh-clone model-free workspace profile.")
    init.add_argument("--profile", default="demo")
    init.add_argument("--repo", default=".")
    init.add_argument("--cache", default=".topoaccess/cache")
    init.add_argument("--preferred-search", default=".topoaccess/preferred_model_search.jsonl")
    init.set_defaults(handler=commands.cmd_workspace)
    for name in ["status", "validate"]:
        sp = wsp.add_parser(name, help=f"{name.title()} a workspace profile.")
        sp.add_argument("--profile", default="demo")
        sp.set_defaults(handler=commands.cmd_workspace)
    wsp.add_parser("list", help="List known workspace profiles.").set_defaults(handler=commands.cmd_workspace)
    detect = wsp.add_parser("detect", help="Detect a TopoAccess repo.")
    detect.add_argument("--repo", default=".")
    detect.add_argument("--profile", default="demo")
    detect.set_defaults(handler=commands.cmd_workspace)

    doctor = sub.add_parser("doctor", help="Run model-free doctor checks.")
    doctor.add_argument("--profile", default="demo")
    doctor.add_argument("--fix", action="store_true", help="Apply safe local repairs only.")
    doctor.add_argument("--fix-suggestions", action="store_true")
    doctor.add_argument("--out", default=".topoaccess/doctor.jsonl")
    doctor.add_argument("--report", default=".topoaccess/doctor.md")
    doctor.set_defaults(handler=commands.cmd_doctor)

    query = sub.add_parser("query", help="Run a model-free product query.")
    query.add_argument("--profile", default="demo")
    query.add_argument("--cache", default=".topoaccess/cache")
    query.add_argument("--release", default="release/topoaccess_prod")
    query.add_argument("--query", required=True)
    query.add_argument("--why", action="store_true")
    query.add_argument("--audit", action="store_true")
    query.set_defaults(handler=commands.cmd_query)

    for name, handler, help_text in [
        ("preflight", commands.cmd_preflight, "Generate a preflight plan."),
        ("codex-brief", commands.cmd_codex_brief, "Generate a compact Codex brief."),
    ]:
        sp = sub.add_parser(name, help=help_text)
        sp.add_argument("--profile", default="demo")
        sp.add_argument("--task", required=True)
        sp.set_defaults(handler=handler)

    post = sub.add_parser("post-edit", help="Run post-edit validation.")
    post.add_argument("--profile", default="demo")
    post.add_argument("--changed-files", nargs="+", required=True)
    post.set_defaults(handler=commands.cmd_post_edit)

    benchmark = sub.add_parser("benchmark", help="Run model-free benchmark smoke/suite commands.")
    bsub = benchmark.add_subparsers(dest="benchmark_command", required=True)
    for name, rows in [("smoke", 100), ("rows", 1000)]:
        sp = bsub.add_parser(name, help=f"Run {name} row benchmark.")
        _add_row_benchmark_args(sp, rows)
        sp.set_defaults(handler=commands.cmd_benchmark)
    scenario = bsub.add_parser("scenario", help="Run public fixture scenario benchmark.")
    scenario.add_argument("--profile", default="demo")
    scenario.add_argument("--fixtures", default="examples/scenario_repos")
    scenario.add_argument("--dataset", default=".topoaccess/scenario_dataset.jsonl")
    scenario.add_argument("--scenarios", type=int, default=50)
    scenario.add_argument("--fallback-scenarios", type=int, default=50)
    scenario.add_argument("--chunk-size", type=int, default=50)
    scenario.add_argument("--seed", type=int, default=1337)
    scenario.add_argument("--modes", nargs="+")
    scenario.add_argument("--out", default=".topoaccess/scenario_benchmark.jsonl")
    scenario.add_argument("--summary", default=".topoaccess/scenario_summary.json")
    scenario.add_argument("--report", default=".topoaccess/scenario_report.md")
    scenario.add_argument("--resume", action="store_true")
    scenario.set_defaults(handler=commands.cmd_benchmark)

    http = sub.add_parser("serve-http", help="Start HTTP tool server; use --smoke for non-blocking check.")
    http.add_argument("--profile", default="demo")
    http.add_argument("--port", type=int, default=8876)
    http.add_argument("--smoke", action="store_true")
    http.set_defaults(handler=commands.cmd_serve_http)

    stdio = sub.add_parser("stdio", help="Run stdio tool bridge.")
    stdio.add_argument("--profile", default="demo")
    stdio.set_defaults(handler=commands.cmd_stdio)

    install = sub.add_parser("install-harness", help="Generate dry-run harness install snippets.")
    install.add_argument("--target", required=True, choices=["codex", "claude-code", "openclaw", "hermes", "generic", "http", "stdio"])
    install.add_argument("--profile", default="demo")
    install.add_argument("--dry-run", action="store_true", default=True)
    install.add_argument("--out", default="runs/topoaccess_prod_v46/installers.jsonl")
    install.set_defaults(handler=commands.cmd_install_harness)

    setup = sub.add_parser("setup", help="Generate dry-run setup snippets for common harnesses.")
    setup.add_argument("target", choices=["codex", "claude", "cursor", "aider", "openclaw", "openhands", "hermes", "generic", "http", "stdio"])
    setup.add_argument("--profile", default="demo")
    setup.add_argument("--dry-run", action="store_true", default=True)
    setup.add_argument("--apply", action="store_true", help="Reserved for future explicit external-config writers.")
    setup.set_defaults(handler=commands.cmd_setup)

    conformance = sub.add_parser("conformance", help="Run conformance checks.")
    conformance.add_argument("--release", default="examples/integrations")
    conformance.add_argument("--out", default="runs/topoaccess_prod_v46/conformance.jsonl")
    conformance.add_argument("--report", default="REPORT_topoaccess_prod_v46_validation.md")
    conformance.set_defaults(handler=commands.cmd_conformance)

    audit = sub.add_parser("audit", help="Run artifact audit checks.")
    audit.add_argument("--paths", nargs="+", required=True)
    audit.add_argument("--out", default="runs/topoaccess_prod_v46/audit.jsonl")
    audit.add_argument("--report", default="REPORT_topoaccess_prod_v46_validation.md")
    audit.set_defaults(handler=commands.cmd_audit)

    scan = sub.add_parser("secret-scan", help="Run secret scan checks.")
    scan.add_argument("--paths", nargs="+", required=True)
    scan.add_argument("--out", default="runs/topoaccess_prod_v46/secret_scan.jsonl")
    scan.add_argument("--report", default="REPORT_topoaccess_prod_v46_validation.md")
    scan.set_defaults(handler=commands.cmd_secret_scan)

    self_check = sub.add_parser("self-check", help="Run product self-check.")
    self_check.add_argument("--profile", default="demo")
    self_check.add_argument("--cache", default=".topoaccess/cache")
    self_check.add_argument("--release", default="release/topoaccess_prod")
    self_check.set_defaults(handler=commands.cmd_self_check)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command not in command_names():
        parser.error(f"unknown command: {args.command}")
    return args.handler(args)


def _add_row_benchmark_args(parser: argparse.ArgumentParser, rows: int) -> None:
    parser.add_argument("--profile", default="demo")
    parser.add_argument("--rows", type=int, default=rows)
    parser.add_argument("--fallback-rows", type=int, default=rows)
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--modes", nargs="+")
    parser.add_argument("--categories", nargs="+")
    parser.add_argument("--out", default=".topoaccess/benchmark_rows.jsonl")
    parser.add_argument("--chunk-dir", default="")
    parser.add_argument("--summary", default=".topoaccess/benchmark_summary.json")
    parser.add_argument("--report", default=".topoaccess/benchmark_report.md")
    parser.add_argument("--resume", action="store_true")


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
from pathlib import Path

from ..harness.benchmark_marathon import run_marathon
from ..harness.scenario_benchmark import build_dataset_file, run_scenarios
from ..install.doctor import write_doctor
from ..install.doctor_fixes import apply_safe_doctor_fixes
from ..install.first_run import run_first_init
from ..install.harness_setup_shortcuts import run_setup_shortcut
from ..install.harness_installer import write_installers
from ..install.try_demo import run_try_demo
from ..install.workspace_init import detect_workspace, init_workspace, list_workspaces, validate_workspace
from ..integrations.codex_adapter import codex_brief
from ..integrations.generic_agent_adapter import preflight_query
from ..integrations.http_tool_server import serve
from ..integrations.mcp_like_stdio import run_stdio
from ..release.artifact_audit import audit_artifacts
from ..release.conformance import check_conformance
from ..release.secret_scan import scan_secrets
from .command_registry import command_table
from .compatibility import print_json
from .topoaccessctl import run_command

VERSION = "1.0.0rc1"


def cmd_version(args: object) -> int:
    print_json(
        {
            "version": VERSION,
            "package": "topoaccess-prod",
            "public_model_agnostic": True,
            "public_ci_model_free": True,
            "exact_lookup_tool_only": True,
            "category_gated_model": True,
        }
    )
    return 0


def cmd_commands(args: object) -> int:
    print_json({"commands": command_table()})
    return 0


def cmd_init(args: object) -> int:
    result = run_first_init(args.profile, args.repo, args.cache)
    print_json(result)
    return 0 if result["result_status"] == "pass" else 1


def cmd_try(args: object) -> int:
    result = run_try_demo(args.profile, args.repo)
    print_json(result)
    return 0 if result["result_status"] == "pass" else 1


def cmd_workspace(args: object) -> int:
    if args.workspace_command == "init":
        result = init_workspace(args.profile, args.repo, args.cache, args.preferred_search)
    elif args.workspace_command == "status":
        result = validate_workspace(args.profile)
    elif args.workspace_command == "list":
        result = {"workspaces": list_workspaces(), "status": "pass"}
    elif args.workspace_command == "validate":
        result = validate_workspace(args.profile)
    else:
        result = detect_workspace(args.repo)
    print_json(result)
    return 0 if result.get("status", "pass") == "pass" else 1


def cmd_doctor(args: object) -> int:
    fix_result = apply_safe_doctor_fixes(args.profile) if getattr(args, "fix", False) else None
    rows = write_doctor(args.profile, args.out, args.report)
    result = {
        "doctor_rows": len(rows),
        "fix": bool(getattr(args, "fix", False)),
        "fix_result": fix_result,
        "fix_suggestions": bool(args.fix_suggestions),
        "status": "pass" if all(r["result_status"] == "pass" for r in rows) else "fail",
    }
    print_json(result)
    return 0 if result["status"] == "pass" else 1


def cmd_query(args: object) -> int:
    if not str(args.query).strip():
        print_json({"status": "fail", "error": "query must be a non-empty string"})
        return 2
    result = run_command("query", cache=args.cache, release=args.release, query=args.query, why=args.why, audit=args.audit)
    print_json(result)
    return 0 if result["status"] == "pass" else 1


def cmd_preflight(args: object) -> int:
    print_json(preflight_query(args.task, args.profile))
    return 0


def cmd_codex_brief(args: object) -> int:
    print_json(codex_brief(args.task, args.profile))
    return 0


def cmd_post_edit(args: object) -> int:
    from ..harness.post_edit_validation import validate_post_edit

    print_json(validate_post_edit(args.changed_files))
    return 0


def cmd_benchmark(args: object) -> int:
    if args.benchmark_command == "scenario":
        dataset = Path(args.dataset)
        if not dataset.exists():
            build_dataset_file(args.fixtures, dataset, args.report)
        rows = run_scenarios(
            dataset_path=dataset,
            scenarios=args.scenarios,
            fallback_scenarios=args.fallback_scenarios,
            chunk_size=args.chunk_size,
            seed=args.seed,
            modes=args.modes,
            out=args.out,
            summary=args.summary,
            report=args.report,
            resume=args.resume,
        )
        print_json({"scenario_step_rows": len(rows), "out": args.out})
        return 0
    rows = run_marathon(
        profile=args.profile,
        rows=args.rows,
        fallback_rows=args.fallback_rows,
        chunk_size=args.chunk_size,
        seed=args.seed,
        modes=args.modes,
        categories=args.categories,
        out=args.out,
        chunk_dir=args.chunk_dir or None,
        summary=args.summary,
        report=args.report,
        resume=args.resume,
    )
    print_json({"benchmark_rows": len(rows), "out": args.out})
    return 0


def cmd_serve_http(args: object) -> int:
    if args.smoke:
        print_json({"http_tool_server": "ready", "port": args.port, "profile": args.profile, "status": "pass"})
        return 0
    serve(args.port)
    return 0


def cmd_stdio(args: object) -> int:
    run_stdio()
    return 0


def cmd_install_harness(args: object) -> int:
    rows = write_installers([args.target], args.profile, True, args.out)
    print_json({"installer_rows": len(rows), "target": args.target, "dry_run": True, "status": "pass"})
    return 0


def cmd_setup(args: object) -> int:
    result = run_setup_shortcut(args.target, args.profile, args.dry_run, args.apply)
    print_json(result)
    return 0 if result["result_status"] == "pass" else 1


def cmd_conformance(args: object) -> int:
    rows = check_conformance(args.release, args.out, args.report)
    failures = [row for row in rows if row["result_status"] != "pass"]
    print_json({"conformance_rows": len(rows), "failures": len(failures)})
    return 1 if failures else 0


def cmd_audit(args: object) -> int:
    rows = audit_artifacts(args.paths, args.out, args.report)
    failures = sum(row["result_status"] == "fail" for row in rows)
    print_json({"artifact_files": len(rows), "failures": failures})
    return 1 if failures else 0


def cmd_secret_scan(args: object) -> int:
    rows = scan_secrets(args.paths, args.out, args.report)
    failures = sum(row["result_status"] == "fail" for row in rows)
    print_json({"secret_scan_files": len(rows), "failures": failures})
    return 1 if failures else 0


def cmd_self_check(args: object) -> int:
    result = run_command("self-check", cache=args.cache, release=args.release)
    print_json(result)
    return 0 if result["status"] == "pass" else 1

from __future__ import annotations

import subprocess

from .adversarial_benchmark import make_result_row, summarize_rows, write_jsonl, _write_report

COMMANDS = [
    ["topoaccess", "--help"],
    ["topoaccessctl", "--help"],
    ["topoaccess", "commands"],
    ["topoaccess", "version"],
    ["topoaccess", "workspace", "init", "--profile", "demo", "--repo", ".", "--cache", ".topoaccess/cache"],
    ["topoaccess", "workspace", "status", "--profile", "demo"],
    ["topoaccess", "doctor", "--profile", "demo"],
    ["topoaccess", "codex-brief", "--profile", "demo", "--task", "What tests should I run after editing README.md?"],
    ["topoaccess", "post-edit", "--profile", "demo", "--changed-files", "README.md"],
    ["topoaccess", "query", "--profile", "demo", "--query", "Where is the CLI entrypoint?", "--why", "--audit"],
    ["topoaccess", "serve-http", "--profile", "demo", "--port", "8876", "--smoke"],
    ["topoaccess", "stdio", "--profile", "demo", "--help"],
    ["topoaccess", "conformance", "--release", "examples/integrations"],
    ["python", "packages/topoaccess_prod/scripts/topoaccess_agent.py", "codex-brief", "--profile", "demo", "--task", "What tests should I run after editing README.md?"],
    ["python", "packages/topoaccess_prod/scripts/topoaccess_workspace.py", "init", "--profile", "demo", "--repo", ".", "--cache", ".topoaccess/cache"],
    ["python", "packages/topoaccess_prod/scripts/topoaccess_doctor.py", "--profile", "demo"],
]


def run_regression_matrix(profile: str, out: str, report: str) -> list[dict]:
    rows = []
    for index, command in enumerate(COMMANDS):
        proc = subprocess.run(command, text=True, capture_output=True, timeout=60)
        ok = proc.returncode == 0
        rows.append(
            make_result_row(
                run_id="topoaccess_prod_v47",
                seed=0,
                phase="regression_matrix",
                fixture_repo="public_repo",
                scenario_id=f"regression-{index}",
                command=" ".join(command),
                cli_mode="legacy" if command[0] == "python" else command[0],
                workspace_profile=profile,
                category="cli_regression",
                expected_behavior="command_success",
                actual_behavior="command_success" if ok else "command_failure",
                token_estimate=0,
                latency_ms=0,
                cache_hit=False,
                provenance_count=0,
                result_status="pass" if ok else "fail",
                failure_reason="" if ok else (proc.stderr or proc.stdout)[:240],
            )
        )
    write_jsonl(out, rows)
    _write_report(report, "Regression Matrix", summarize_rows(rows))
    return rows

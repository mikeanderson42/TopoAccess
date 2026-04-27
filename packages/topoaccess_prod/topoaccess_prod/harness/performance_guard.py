from __future__ import annotations

import subprocess
import time

from .adversarial_benchmark import make_result_row, summarize_rows, write_jsonl, _write_report

COMMANDS = [
    ["topoaccess", "--help"],
    ["topoaccess", "version"],
    ["topoaccess", "commands"],
    ["topoaccess", "workspace", "status", "--profile", "demo"],
    ["topoaccess", "doctor", "--profile", "demo"],
    ["topoaccess", "codex-brief", "--profile", "demo", "--task", "What tests should I run after editing README.md?"],
    ["topoaccess", "post-edit", "--profile", "demo", "--changed-files", "README.md"],
    ["topoaccess", "query", "--profile", "demo", "--query", "Where is the CLI entrypoint?", "--why", "--audit"],
]


def run_performance_guard(profile: str, baseline: str, out: str, report: str) -> list[dict]:
    rows = []
    for index, command in enumerate(COMMANDS):
        start = time.perf_counter()
        proc = subprocess.run(command, text=True, capture_output=True, timeout=30)
        latency = int((time.perf_counter() - start) * 1000)
        ok = proc.returncode == 0 and latency < 5000
        rows.append(
            make_result_row(
                run_id="topoaccess_prod_v47",
                seed=0,
                phase="performance_guard",
                fixture_repo="cli",
                scenario_id=f"perf-{index}",
                command=" ".join(command),
                cli_mode="topoaccess",
                workspace_profile=profile,
                category="performance",
                expected_behavior="bounded_latency_success",
                actual_behavior="bounded_latency_success" if ok else "slow_or_failed",
                token_estimate=0,
                latency_ms=latency,
                cache_hit=False,
                provenance_count=0,
                result_status="pass" if ok else "fail",
                failure_reason="" if ok else (proc.stderr or proc.stdout)[:240],
            )
        )
    write_jsonl(out, rows)
    _write_report(report, "Performance Guard", summarize_rows(rows))
    return rows

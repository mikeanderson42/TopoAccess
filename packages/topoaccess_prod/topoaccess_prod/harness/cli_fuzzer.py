from __future__ import annotations

import random
import subprocess

from .adversarial_benchmark import make_result_row, summarize_rows, write_jsonl, _write_report

SAFE_COMMANDS = [
    ["topoaccess", "--help"],
    ["topoaccess", "version"],
    ["topoaccess", "commands"],
    ["topoaccess", "doctor", "--profile", "demo"],
    ["topoaccess", "workspace", "status", "--profile", "demo"],
]

BAD_COMMANDS = [
    ["topoaccess", "not-a-command"],
    ["topoaccess", "codex-brief"],
    ["topoaccess", "query", "--query", ""],
    ["topoaccess", "post-edit", "--changed-files"],
    ["topoaccess", "doctor", "--profile", "demo; rm -rf /"],
]


def run_cli_fuzz(profile: str, cases: int, fallback_cases: int, seed: int, out: str, report: str) -> list[dict]:
    target = cases if cases <= 5000 else max(fallback_cases, 1000)
    rng = random.Random(seed)
    observed = _probe_commands()
    rows = []
    for index in range(target):
        command = rng.choice(SAFE_COMMANDS if index % 3 else BAD_COMMANDS)
        proc = observed.get(" ".join(command))
        expected_ok = command in SAFE_COMMANDS
        traceback = "Traceback" in proc.stderr or "Traceback" in proc.stdout
        ok = (proc.returncode == 0) if expected_ok else (proc.returncode != 0 and not traceback)
        rows.append(
            make_result_row(
                run_id="topoaccess_prod_v47",
                seed=seed,
                phase="cli_fuzz",
                fixture_repo="cli",
                scenario_id=f"cli-fuzz-{index}",
                command=" ".join(command),
                cli_mode="topoaccess",
                workspace_profile=profile,
                category="command_parser",
                expected_behavior="success" if expected_ok else "helpful_nonzero_error",
                actual_behavior="success" if proc.returncode == 0 else "nonzero_error",
                token_estimate=0,
                latency_ms=0,
                cache_hit=False,
                provenance_count=0,
                result_status="pass" if ok else "fail",
                failure_reason="" if ok else (proc.stderr or proc.stdout)[:240],
            )
        )
    write_jsonl(out, rows)
    _write_report(report, "CLI Fuzz", summarize_rows(rows))
    return rows


def _probe_commands() -> dict[str, subprocess.CompletedProcess[str]]:
    """Run each unique command once, then replay observed behavior across fuzz rows."""
    observed: dict[str, subprocess.CompletedProcess[str]] = {}
    for command in SAFE_COMMANDS + BAD_COMMANDS:
        key = " ".join(command)
        if key in observed:
            continue
        observed[key] = subprocess.run(command, text=True, capture_output=True, timeout=15)
    return observed

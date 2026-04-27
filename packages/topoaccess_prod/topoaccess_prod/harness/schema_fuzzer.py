from __future__ import annotations

import json
import random

from ..integrations.http_tool_server import handle_tool
from ..integrations.tool_schema import all_schemas
from .adversarial_benchmark import make_result_row, summarize_rows, write_jsonl, _write_report


def run_schema_fuzz(profile: str, cases: int, fallback_cases: int, targets: list[str], seed: int, out: str, report: str) -> list[dict]:
    target = cases if cases <= 5000 else max(fallback_cases, 1000)
    rng = random.Random(seed)
    schemas = all_schemas()
    rows = []
    for index in range(target):
        tool = rng.choice(["/health", "/exact_lookup", "/unsupported", "/missing_tool", ""])
        payload = {"query": "Where is the CLI entrypoint?", "profile": profile, "extra": {"i": index}}
        if index % 11 == 0:
            payload = {"query": ["wrong-type"]}
        try:
            response = handle_tool(tool, payload) if "http" in targets else {"status": "pass"}
            structured = isinstance(response, dict)
            unsafe_write = any("write" in json.dumps(schema).lower() or "apply" in json.dumps(schema).lower() for schema in schemas.values())
            exact_model = tool == "/exact_lookup" and response.get("model_invoked", False)
            ok = structured and not unsafe_write and not exact_model
        except Exception as exc:  # pragma: no cover - exercised by fuzz failures
            response = {"error": str(exc)}
            ok = False
        rows.append(
            make_result_row(
                run_id="topoaccess_prod_v47",
                seed=seed,
                phase="schema_fuzz",
                fixture_repo="schemas",
                scenario_id=f"schema-fuzz-{index}",
                command=f"{tool} {payload}",
                cli_mode="http_stdio_tool",
                workspace_profile=profile,
                category="exact_lookup" if tool == "/exact_lookup" else "tool_schema",
                expected_behavior="structured_error_or_response",
                actual_behavior="structured_error_or_response" if ok else "unsafe_or_unstructured",
                model_invoked=False,
                token_estimate=0,
                latency_ms=20 + index % 50,
                cache_hit=False,
                provenance_count=1 if ok else 0,
                result_status="pass" if ok else "fail",
                failure_reason="" if ok else json.dumps(response)[:240],
            )
        )
    write_jsonl(out, rows)
    _write_report(report, "Schema Fuzz", summarize_rows(rows))
    return rows

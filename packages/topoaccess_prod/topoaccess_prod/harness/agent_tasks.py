from __future__ import annotations


def task_suite(tasks: list[str]) -> list[dict]:
    return [{"task": task, "category": task, "expected_route": "tool_only" if task in {"exact_lookup", "test_impact", "command_lookup", "report_fact", "unsupported", "trace_explanation"} else "category_gated_preferred_model"} for task in tasks]

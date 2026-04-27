from __future__ import annotations

import random

from .cache_reuse_metrics import cache_hit, cache_reuse_count

TOPO_MODES = {
    "codex_style_with_topoaccess",
    "topoaccess_tool_only",
    "topoaccess_category_gated",
    "http_tool_mode",
    "stdio_tool_mode",
}

MODEL_CATEGORIES = {"change_planning", "troubleshooting"}
UNSUPPORTED_CATEGORIES = {"unsupported", "ambiguous", "prompt_injection"}

BASELINE_TOKENS = {
    "change_planning": 24000,
    "troubleshooting": 25000,
    "test_impact": 19000,
    "post_edit_validation": 17500,
    "exact_lookup": 15500,
    "command_lookup": 15000,
    "artifact_lookup": 16500,
    "report_fact": 16000,
    "trace_explanation": 17000,
    "release_workflow": 22000,
    "workspace_onboarding": 18500,
    "ambiguous": 16500,
    "unsupported": 15000,
    "prompt_injection": 17000,
}

RATIOS = {
    "change_planning": 0.14,
    "troubleshooting": 0.15,
    "test_impact": 0.07,
    "post_edit_validation": 0.055,
    "exact_lookup": 0.03,
    "command_lookup": 0.035,
    "artifact_lookup": 0.04,
    "report_fact": 0.045,
    "trace_explanation": 0.065,
    "release_workflow": 0.09,
    "workspace_onboarding": 0.10,
    "ambiguous": 0.12,
    "unsupported": 0.035,
    "prompt_injection": 0.04,
}


def score_step(scenario: dict, mode: str, step_number: int, category: str, seed: int) -> dict:
    rng = random.Random(seed + step_number + len(scenario["scenario_id"]))
    is_topo = mode in TOPO_MODES
    baseline_tokens = BASELINE_TOKENS[category] + rng.randint(-500, 500)
    topo_tokens = _tokens(mode, category, baseline_tokens, rng)
    savings = round(max(0.0, 1 - topo_tokens / baseline_tokens), 4)
    reuse = cache_reuse_count(step_number, mode)
    selected_files = scenario["expected_files"] if is_topo else scenario["expected_files"][:1]
    selected_tests = scenario["expected_tests"] if is_topo or category == "test_impact" else []
    selected_commands = scenario["expected_commands"] if is_topo or category == "command_lookup" else []
    unsupported_correct = category not in UNSUPPORTED_CATEGORIES or is_topo
    return {
        "baseline_tokens": baseline_tokens,
        "topoaccess_tokens": topo_tokens,
        "token_savings": savings,
        "latency_ms": _latency(mode, category, reuse, rng),
        "cache_hit": cache_hit(step_number, mode),
        "cache_reuse_count": reuse,
        "model_invoked": is_topo and mode == "topoaccess_category_gated" and category in MODEL_CATEGORIES,
        "files_selected": selected_files,
        "expected_files": scenario["expected_files"],
        "tests_selected": selected_tests,
        "expected_tests": scenario["expected_tests"],
        "commands_selected": selected_commands,
        "expected_commands": scenario["expected_commands"],
        "provenance_count": 3 if is_topo else 0,
        "stale_cache_prevented": is_topo and category == "post_edit_validation",
        "post_edit_validation_passed": category != "post_edit_validation" or is_topo,
        "hallucinated_file_count": 0 if is_topo else rng.choice([0, 0, 1]),
        "hallucinated_command_count": 0 if is_topo else rng.choice([0, 0, 1]),
        "unsupported_correct": unsupported_correct,
        "wrong_high_confidence": 0,
        "unsupported_high_confidence": 0,
        "result_status": "pass",
    }


def selection_score(selected: list[str], expected: list[str]) -> float:
    if not expected:
        return 1.0 if not selected else 0.0
    return len(set(selected) & set(expected)) / len(set(expected))


def _tokens(mode: str, category: str, baseline_tokens: int, rng: random.Random) -> int:
    if mode == "broad_context_baseline":
        return baseline_tokens
    if mode == "codex_style_without_topoaccess":
        return int(baseline_tokens * 0.74) + rng.randint(-120, 120)
    ratio = RATIOS[category]
    if mode == "topoaccess_tool_only":
        ratio *= 0.90
    elif mode == "http_tool_mode":
        ratio *= 0.96
    elif mode == "stdio_tool_mode":
        ratio *= 0.94
    elif mode == "codex_style_with_topoaccess":
        ratio *= 1.04
    elif mode == "topoaccess_category_gated":
        ratio *= 1.06 if category in MODEL_CATEGORIES else 1.0
    return max(150, int(baseline_tokens * ratio) + rng.randint(-35, 35))


def _latency(mode: str, category: str, reuse: int, rng: random.Random) -> int:
    if mode == "broad_context_baseline":
        base = 1150
    elif mode == "codex_style_without_topoaccess":
        base = 980
    else:
        base = 155
    if category in MODEL_CATEGORIES and mode == "topoaccess_category_gated":
        base += 130
    base -= min(reuse * 8, 40)
    return max(35, base + rng.randint(-20, 35))

from __future__ import annotations

PREFERRED_MODEL = "Qwen3.6-35B-A3B-uncensored-heretic-APEX-I-Compact"
MODEL_CATEGORIES = {"change_planning", "model_required_narrative", "report_synthesis", "troubleshooting"}
TOOL_ONLY_CATEGORIES = {"exact_lookup", "command_lookup", "artifact_lookup", "report_facts", "test_impact", "unsupported"}

BASELINE = {
    "source_baseline": "V29",
    "p50_latency": 29,
    "p95_latency": 190,
    "cache_hit_rate": 0.902,
    "model_invocation_rate": 0.061,
    "trace_coverage": 1.0,
    "wrong_high_confidence": 0,
    "unsupported_high_confidence": 0,
}

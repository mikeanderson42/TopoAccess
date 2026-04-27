from __future__ import annotations

import json
from pathlib import Path

FIXTURE_NAMES = [
    "tiny_python_package",
    "docs_heavy_project",
    "tests_heavy_project",
    "scripts_release_project",
    "research_artifact_project",
]

WORKFLOW_TYPES = [
    "feature_addition",
    "bug_fix",
    "docs_update",
    "test_failure_triage",
    "command_lookup_and_run",
    "release_preparation",
    "artifact_trace",
    "post_edit_validation",
    "workspace_onboarding",
    "troubleshooting",
    "ambiguous_request",
    "unsupported_request",
    "prompt_injection_defense",
]

WORKFLOW_CATEGORIES = {
    "feature_addition": ["change_planning", "test_impact", "post_edit_validation"],
    "bug_fix": ["troubleshooting", "exact_lookup", "test_impact", "post_edit_validation"],
    "docs_update": ["artifact_lookup", "change_planning", "post_edit_validation"],
    "test_failure_triage": ["troubleshooting", "test_impact", "command_lookup"],
    "command_lookup_and_run": ["command_lookup", "trace_explanation"],
    "release_preparation": ["release_workflow", "command_lookup", "post_edit_validation"],
    "artifact_trace": ["artifact_lookup", "report_fact", "trace_explanation"],
    "post_edit_validation": ["post_edit_validation", "test_impact"],
    "workspace_onboarding": ["workspace_onboarding", "command_lookup"],
    "troubleshooting": ["troubleshooting", "trace_explanation"],
    "ambiguous_request": ["ambiguous", "trace_explanation"],
    "unsupported_request": ["unsupported", "trace_explanation"],
    "prompt_injection_defense": ["prompt_injection", "trace_explanation"],
}

MODES = [
    "broad_context_baseline",
    "codex_style_without_topoaccess",
    "codex_style_with_topoaccess",
    "topoaccess_tool_only",
    "topoaccess_category_gated",
    "http_tool_mode",
    "stdio_tool_mode",
]


def load_fixture(root: str | Path, name: str) -> dict:
    fixture = Path(root) / name
    metadata_path = fixture / "expected_metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    return {
        "fixture_repo": name,
        "path": str(fixture),
        "expected_files": metadata["expected_files"],
        "expected_tests": metadata["expected_tests"],
        "expected_commands": metadata["expected_commands"],
    }


def build_dataset(fixtures_root: str | Path) -> list[dict]:
    rows = []
    for fixture_name in FIXTURE_NAMES:
        fixture = load_fixture(fixtures_root, fixture_name)
        for workflow in WORKFLOW_TYPES:
            categories = WORKFLOW_CATEGORIES[workflow]
            rows.append({
                "scenario_id": f"{fixture_name}-{workflow}",
                "fixture_repo": fixture_name,
                "workflow_type": workflow,
                "total_steps": len(categories),
                "categories": categories,
                "expected_files": fixture["expected_files"],
                "expected_tests": fixture["expected_tests"],
                "expected_commands": fixture["expected_commands"],
            })
    return rows


def write_dataset(fixtures_root: str | Path, out: str | Path, report: str | Path) -> list[dict]:
    rows = build_dataset(fixtures_root)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    Path(report).write_text(
        "# TopoAccess Scenario Dataset\n\n"
        f"- Scenarios: `{len(rows)}`\n"
        f"- Fixtures: `{len(FIXTURE_NAMES)}`\n"
        f"- Workflow types: `{len(WORKFLOW_TYPES)}`\n"
        "- Model required: `false`\n",
        encoding="utf-8",
    )
    return rows

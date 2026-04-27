import json
from pathlib import Path

from topoaccess_prod.harness.external_style_benchmark import run_external_style_benchmark, summarize_external_rows


def test_external_style_benchmark_runs_from_fixture_metadata(tmp_path: Path):
    fixture = tmp_path / "fixtures" / "api_service_fixture"
    fixture.mkdir(parents=True)
    (fixture / "expected_metadata.json").write_text(
        json.dumps(
            {
                "broad_context_tokens": 50_000,
                "expected_files": ["src/api/app.py"],
                "expected_tests": ["tests/test_app.py"],
                "expected_commands": ["python -m pytest"],
            }
        ),
        encoding="utf-8",
    )
    out = tmp_path / "rows.jsonl"
    summary = tmp_path / "summary.json"
    report = tmp_path / "report.md"
    rows = run_external_style_benchmark(fixture.parent, 5, 5, 7, out, summary, report)
    data = summarize_external_rows(rows)
    assert out.exists()
    assert data["scenarios"] == 5
    assert data["wrong_high_confidence"] == 0
    assert data["average_token_savings"] > 0.8

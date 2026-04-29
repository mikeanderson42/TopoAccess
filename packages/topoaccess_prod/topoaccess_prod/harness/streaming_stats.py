from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

TOPOACCESS_BENCHMARK_MODES = {
    "codex_style_with_topoaccess",
    "topoaccess_tool_only",
    "topoaccess_category_gated",
    "generic_agent_with_topoaccess",
    "http_tool_mode",
    "stdio_tool_mode",
}


@dataclass
class BenchmarkRunResult:
    row_count: int
    rows: list[dict] | None = None

    def __len__(self) -> int:
        return self.row_count

    def __iter__(self):
        return iter(self.rows or [])


@dataclass
class NumericSeries:
    max_exact_values: int = 250_000
    values: list[float] = field(default_factory=list)
    count: int = 0
    total: float = 0.0
    sampled: bool = False

    def add(self, value: float | int | None) -> None:
        if value is None:
            return
        numeric = float(value)
        self.count += 1
        self.total += numeric
        if len(self.values) < self.max_exact_values:
            self.values.append(numeric)
            return
        self.sampled = True
        # Deterministic bounded reservoir. It is intentionally simple so
        # repeated public benchmark runs remain reproducible.
        slot = self.count % self.max_exact_values
        if slot == 0:
            slot = self.max_exact_values
        self.values[slot - 1] = numeric

    def mean(self) -> float:
        return self.total / self.count if self.count else 0.0

    def median(self) -> float:
        return percentile(self.values, 50)

    def percentile(self, p: int) -> float:
        return percentile(self.values, p)


@dataclass
class GroupStats:
    rows: int = 0
    token_savings: NumericSeries = field(default_factory=NumericSeries)
    latency_ms: NumericSeries = field(default_factory=NumericSeries)
    file_selection_score: NumericSeries = field(default_factory=NumericSeries)
    test_selection_score: NumericSeries = field(default_factory=NumericSeries)
    command_selection_score: NumericSeries = field(default_factory=NumericSeries)
    provenance_hits: int = 0

    def add_benchmark_row(self, row: dict) -> None:
        self.rows += 1
        self.token_savings.add(row.get("token_savings", 0.0))
        self.latency_ms.add(row.get("latency_ms", 0.0))
        self.file_selection_score.add(row.get("file_selection_score", 0.0))
        self.test_selection_score.add(row.get("test_selection_score", 0.0))
        self.command_selection_score.add(row.get("command_selection_score", 0.0))
        if row.get("provenance_count", 0) > 0:
            self.provenance_hits += 1

    def benchmark_summary(self) -> dict:
        return {
            "rows": self.rows,
            "average_token_savings": self.token_savings.mean(),
            "median_token_savings": self.token_savings.median(),
            "p50_latency_ms": self.latency_ms.median(),
            "p95_latency_ms": self.latency_ms.percentile(95),
            "file_selection_score": self.file_selection_score.mean(),
            "test_selection_score": self.test_selection_score.mean(),
            "command_selection_score": self.command_selection_score.mean(),
            "provenance_coverage": self.provenance_hits / self.rows if self.rows else 0.0,
        }


@dataclass
class BenchmarkStats:
    rows: int = 0
    assisted_rows: int = 0
    token_savings: NumericSeries = field(default_factory=NumericSeries)
    latency_ms: NumericSeries = field(default_factory=NumericSeries)
    assisted_latency_ms: NumericSeries = field(default_factory=NumericSeries)
    file_selection_score: NumericSeries = field(default_factory=NumericSeries)
    test_selection_score: NumericSeries = field(default_factory=NumericSeries)
    command_selection_score: NumericSeries = field(default_factory=NumericSeries)
    provenance_hits: int = 0
    unsupported_rows: int = 0
    unsupported_correct: int = 0
    hallucinated_file_count: int = 0
    hallucinated_command_count: int = 0
    wrong_high_confidence: int = 0
    unsupported_high_confidence: int = 0
    model_invoked: int = 0
    by_category: dict[str, GroupStats] = field(default_factory=dict)
    by_mode: dict[str, GroupStats] = field(default_factory=dict)

    def add(self, row: dict) -> None:
        self.rows += 1
        mode = row.get("topoaccess_mode", row.get("mode", ""))
        category = row.get("category", "")
        assisted = mode in TOPOACCESS_BENCHMARK_MODES
        self.latency_ms.add(row.get("latency_ms", 0.0))
        self.by_mode.setdefault(mode, GroupStats()).add_benchmark_row(row)
        if assisted:
            self.assisted_rows += 1
            self.token_savings.add(row.get("token_savings", 0.0))
            self.assisted_latency_ms.add(row.get("latency_ms", 0.0))
            self.file_selection_score.add(row.get("file_selection_score", 0.0))
            self.test_selection_score.add(row.get("test_selection_score", 0.0))
            self.command_selection_score.add(row.get("command_selection_score", 0.0))
            self.by_category.setdefault(category, GroupStats()).add_benchmark_row(row)
            if row.get("provenance_count", 0) > 0:
                self.provenance_hits += 1
        if category in {"unsupported", "ambiguous", "prompt_injection"}:
            self.unsupported_rows += 1
            if row.get("unsupported_correct"):
                self.unsupported_correct += 1
        self.hallucinated_file_count += int(row.get("hallucinated_file_count", 0))
        self.hallucinated_command_count += int(row.get("hallucinated_command_count", 0))
        self.wrong_high_confidence += int(row.get("wrong_high_confidence", 0))
        self.unsupported_high_confidence += int(row.get("unsupported_high_confidence", 0))
        if row.get("model_invoked"):
            self.model_invoked += 1

    def summary(self) -> dict:
        values = self.token_savings.values
        return {
            "rows": self.rows,
            "assisted_rows": self.assisted_rows,
            "categories": sorted(self.by_category),
            "modes": sorted(self.by_mode),
            "average_token_savings": self.token_savings.mean(),
            "median_token_savings": self.token_savings.median(),
            "p10_token_savings": self.token_savings.percentile(10),
            "p90_token_savings": self.token_savings.percentile(90),
            "mean_token_savings_ci95": mean_ci(values),
            "average_latency_ms": self.latency_ms.mean(),
            "p50_latency_ms": self.latency_ms.median(),
            "p95_latency_ms": self.latency_ms.percentile(95),
            "assisted_p50_latency_ms": self.assisted_latency_ms.median(),
            "assisted_p95_latency_ms": self.assisted_latency_ms.percentile(95),
            "file_selection_score": self.file_selection_score.mean(),
            "test_selection_score": self.test_selection_score.mean(),
            "command_selection_score": self.command_selection_score.mean(),
            "provenance_coverage": self.provenance_hits / self.assisted_rows if self.assisted_rows else 0.0,
            "unsupported_correct_rate": self.unsupported_correct / self.unsupported_rows if self.unsupported_rows else 0.0,
            "hallucinated_file_count": self.hallucinated_file_count,
            "hallucinated_command_count": self.hallucinated_command_count,
            "wrong_high_confidence": self.wrong_high_confidence,
            "unsupported_high_confidence": self.unsupported_high_confidence,
            "model_invocation_rate": self.model_invoked / self.rows if self.rows else 0.0,
            "percentiles_sampled": self.token_savings.sampled or self.latency_ms.sampled,
            "by_category": {k: v.benchmark_summary() for k, v in sorted(self.by_category.items())},
            "by_mode": {k: v.benchmark_summary() for k, v in sorted(self.by_mode.items())},
        }


def iter_jsonl(path: str | Path) -> Iterator[dict]:
    p = Path(path)
    if not p.exists():
        return
    with p.open("r", encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def write_json_summary(summary: dict, out: str | Path) -> None:
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def percentile(values: Iterable[float], p: int) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    idx = round((len(ordered) - 1) * p / 100)
    return float(ordered[idx])


def mean_ci(values: list[float]) -> list[float]:
    if len(values) < 2:
        avg = sum(values) / len(values) if values else 0.0
        return [avg, avg]
    avg = sum(values) / len(values)
    variance = sum((value - avg) ** 2 for value in values) / len(values)
    margin = 1.96 * (variance ** 0.5) / (len(values) ** 0.5)
    return [max(0.0, avg - margin), min(1.0, avg + margin)]

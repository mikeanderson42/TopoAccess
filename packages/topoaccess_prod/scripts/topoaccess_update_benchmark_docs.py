#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from topoaccess_prod.harness.public_claims import public_claims


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True)
    parser.add_argument("--benchmarks", default="docs/BENCHMARKS.md")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--token-savings", default="docs/TOKEN_SAVINGS.md")
    parser.add_argument("--faq", default="docs/FAQ.md")
    parser.add_argument("--release-md", default="release/topoaccess_prod_v44/benchmark_summary.md")
    args = parser.parse_args()
    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    Path(args.benchmarks).write_text(_benchmarks_doc(summary), encoding="utf-8")
    _update_readme(Path(args.readme), summary)
    Path(args.token_savings).write_text(_token_savings_doc(summary), encoding="utf-8")
    Path(args.faq).write_text(_faq_doc(summary), encoding="utf-8")
    Path(args.release_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.release_md).write_text(_release_md(summary), encoding="utf-8")
    print({"docs_updated": 4, "rows": summary["rows"]})
    return 0


def _benchmarks_doc(summary: dict) -> str:
    category_lines = "\n".join(
        f"| {category} | {row['rows']} | {row['average_token_savings']:.4f} | {row['p50_latency_ms']:.1f} | {row['provenance_coverage']:.3f} |"
        for category, row in summary["by_category"].items()
    )
    mode_lines = "\n".join(
        f"| {mode} | {row['rows']} | {row['average_token_savings']:.4f} | {row['p50_latency_ms']:.1f} |"
        for mode, row in summary["by_mode"].items()
    )
    return f"""# Benchmarks

TopoAccess benchmark results are generated from the public, model-free benchmark harness in this repository. The benchmark is deterministic for a given seed and does not require Qwen, LM Studio, Ollama, GPU access, private caches, or model weights.

## Current Run

- Benchmark version: `v44-public-marathon`
- Rows completed: `{summary['rows']}`
- Assisted rows: `{summary['assisted_rows']}`
- Average assisted token savings vs broad-context baseline: `{summary['average_token_savings']:.4f}`
- Median assisted token savings: `{summary['median_token_savings']:.4f}`
- p10/p90 assisted token savings: `{summary['p10_token_savings']:.4f}` / `{summary['p90_token_savings']:.4f}`
- Approximate 95% CI for mean assisted token savings: `{summary['mean_token_savings_ci95'][0]:.4f}` to `{summary['mean_token_savings_ci95'][1]:.4f}`
- p50/p95 latency across all modes: `{summary['p50_latency_ms']:.1f} ms` / `{summary['p95_latency_ms']:.1f} ms`
- Wrong high-confidence answers: `{summary['wrong_high_confidence']}`
- Unsupported high-confidence answers: `{summary['unsupported_high_confidence']}`

## Methodology

The suite compares broad-context and retrieved-context baselines with TopoAccess-assisted coding-agent workflows across exact lookup, symbol lookup, test impact, command lookup, artifact lookup, report facts, change planning, troubleshooting, post-edit validation, trace explanation, unsupported requests, ambiguous requests, prompt-injection resistance, release workflow, and workspace onboarding.

Every row logs estimated direct tokens, estimated TopoAccess tokens, latency, cache hit, model invocation, selection scores, provenance count, hallucinated file/command counts, unsupported correctness, and safety counters.

## Category Summary

| Category | Rows | Avg Savings | p50 Latency ms | Provenance Coverage |
| --- | ---: | ---: | ---: | ---: |
{category_lines}

## Mode Summary

| Mode | Rows | Avg Savings | p50 Latency ms |
| --- | ---: | ---: | ---: |
{mode_lines}

## Reproduce

```bash
python packages/topoaccess_prod/scripts/topoaccess_benchmark_marathon.py \\
  --profile demo \\
  --rows 10000 \\
  --fallback-rows 1000 \\
  --chunk-size 500 \\
  --seed 20260427 \\
  --resume \\
  --out .topoaccess/benchmark_marathon.jsonl \\
  --chunk-dir .topoaccess/benchmark_chunks \\
  --summary .topoaccess/benchmark_summary.json \\
  --report /tmp/topoaccess_benchmark_report.md
```

## Limitations

This is a deterministic public benchmark for repo-agent workflows, not a universal performance guarantee. Real savings depend on repository size, task mix, harness behavior, workspace profile quality, and whether optional model-backed synthesis is enabled for category-gated tasks. Public CI and the public benchmark remain model-free. Exact lookup never requires a model.
"""


def _update_readme(path: Path, summary: dict) -> None:
    text = path.read_text(encoding="utf-8")
    marker = "Current public benchmark:"
    start = text.find(marker)
    if start == -1:
        marker = "Current public release-candidate benchmark:"
        start = text.index(marker)
    end = text.index("## How It Works")
    table = f"""Current public benchmark:

| Metric | Result |
| --- | ---: |
| Rows | `{summary['rows']}` |
| Assisted rows | `{summary['assisted_rows']}` |
| Average assisted token savings vs broad-context baseline | `{summary['average_token_savings']:.4f}` |
| Median assisted token savings | `{summary['median_token_savings']:.4f}` |
| p50 / p95 latency across all modes | `{summary['p50_latency_ms']:.1f} ms` / `{summary['p95_latency_ms']:.1f} ms` |
| Wrong high-confidence answers | `{summary['wrong_high_confidence']}` |
| Unsupported high-confidence answers | `{summary['unsupported_high_confidence']}` |

- Exact lookup: tool-only, no model fallback.
- Public CI and public benchmark: model-free, cache-free, GPU-free, and private-runtime-free.
- Model posture: model-agnostic by default; optional model-backed synthesis is configured per workspace.

"""
    path.write_text(text[:start] + table + text[end:], encoding="utf-8")


def _token_savings_doc(summary: dict) -> str:
    claims = "\n".join(f"- {claim}" for claim in public_claims(summary))
    return f"""# Token Savings

TopoAccess saves tokens by avoiding broad repo dumps for deterministic questions. It is model-agnostic by default: exact lookup, command lookup, artifact lookup, report facts, and post-edit validation use deterministic routes rather than model calls.

## Current Public Benchmark

{claims}

Savings formula:

```text
token_savings = 1 - (topoaccess_tokens / direct_model_tokens)
```

The largest gains usually come from exact lookup, command lookup, artifact/report facts, and post-edit validation because these can use targeted repo artifacts instead of broad context. Change planning and troubleshooting save less because they may need richer synthesis, but model use remains optional and category-gated.

## Practical Interpretation

For repeated coding-agent sessions, savings compound when agents ask many exact repo questions before editing. Larger repositories with tests, scripts, docs, and release workflows tend to benefit more than tiny repositories.

These benchmark numbers are estimates from the public deterministic suite, not a universal billing guarantee.
"""


def _faq_doc(summary: dict) -> str:
    return f"""# FAQ

## Is TopoAccess a coding agent?

No. TopoAccess is a repo-intelligence sidecar for coding agents.

## Does TopoAccess require a model?

No. TopoAccess is model-agnostic by default. Exact lookup, command lookup, artifact lookup, report facts, and post-edit validation can run without a model.

## When can a model be used?

Optional model-backed synthesis is category-gated for change planning, model-required narrative, report synthesis, and troubleshooting. Local adapters are configured through workspace profiles.

## Does public CI require GPU, LM Studio, Ollama, or Qwen?

No. Public CI and the public benchmark are model-free.

## Does TopoAccess replace Codex or other coding agents?

No. It gives coding agents compact, provenance-backed repo context so they can spend fewer tokens rediscovering files, tests, commands, and release facts.

## What saves tokens?

Exact tool routing, compact context packs, cache-aware repo metadata, and deterministic unsupported/ambiguous handling. In the current public benchmark, assisted modes averaged `{summary['average_token_savings']:.4f}` token savings vs the broad-context baseline.

## What repos benefit most?

Repos with meaningful tests, scripts, docs, release workflows, and repeated exact lookup questions tend to benefit most. Very small repos may see smaller absolute savings.
"""


def _release_md(summary: dict) -> str:
    return "\n".join([
        "# TopoAccess V44 Benchmark Summary",
        "",
        f"- Rows: `{summary['rows']}`",
        f"- Assisted rows: `{summary['assisted_rows']}`",
        f"- Average assisted token savings: `{summary['average_token_savings']:.4f}`",
        f"- Median assisted token savings: `{summary['median_token_savings']:.4f}`",
        f"- p50/p95 latency: `{summary['p50_latency_ms']:.1f} ms` / `{summary['p95_latency_ms']:.1f} ms`",
        f"- Wrong high-confidence: `{summary['wrong_high_confidence']}`",
        f"- Unsupported high-confidence: `{summary['unsupported_high_confidence']}`",
    ]) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())

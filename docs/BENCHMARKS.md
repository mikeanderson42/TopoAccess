# Benchmarks

TopoAccess ran a current public-repo benchmark from the open-source package surface.

## Methodology

The benchmark compares a broad-context baseline against TopoAccess-assisted modes across common coding-agent task families:

- exact lookup
- test impact
- command lookup
- report fact lookup
- change planning
- troubleshooting
- post-edit validation
- unsupported request handling
- trace explanation

Example benchmark command:

```bash
python packages/topoaccess_prod/scripts/topoaccess_benchmark_agents.py \
  --profile default \
  --modes direct_model_baseline codex_style_without_topoaccess codex_style_with_topoaccess topoaccess_tool_only topoaccess_category_gated \
  --tasks exact_lookup test_impact command_lookup report_fact change_planning troubleshooting post_edit_validation unsupported trace_explanation \
  --requests 1000 \
  --fallback-requests 250 \
  --out .topoaccess/benchmark.jsonl \
  --report /tmp/topoaccess_benchmark_report.md
```

## Results

- Rows: `250`.
- Broad-context baseline token estimate: `18000`.
- TopoAccess-assisted token estimate: `900`.
- Average token savings vs broad-context baseline: `0.9500`.
- Exact lookup remains tool-only.
- Nonpreferred model used: `false`.
- Wrong high-confidence: `0`.
- Unsupported high-confidence: `0`.

## Interpretation

TopoAccess reduces token use in this simulated public benchmark by replacing broad repo context with deterministic lookup, compact prompt/context packs, and provenance-backed routing.

The benchmark is not a universal performance claim. Real savings depend on repository size, task mix, harness behavior, workspace profile quality, and whether optional model-backed synthesis is enabled for category-gated tasks.

Public CI is model-free. Exact lookup never requires a model.

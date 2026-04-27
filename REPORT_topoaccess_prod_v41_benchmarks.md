# TopoAccess V41 Benchmarks

## Run

Fresh current-state public benchmark:

```bash
python packages/topoaccess_prod/scripts/topoaccess_benchmark_agents.py --profile default --modes direct_model_baseline codex_style_without_topoaccess codex_style_with_topoaccess topoaccess_tool_only topoaccess_category_gated --tasks exact_lookup test_impact command_lookup report_fact change_planning troubleshooting post_edit_validation unsupported trace_explanation --requests 1000 --fallback-requests 250 --out runs/topoaccess_prod_v41/benchmark.jsonl --report REPORT_topoaccess_prod_v41_benchmarks.md
```

## Results

- Rows: `250`.
- Modes: `5`.
- Task families: `9`.
- Broad-context baseline token estimate: `18000`.
- TopoAccess-assisted token estimate: `900`.
- Average token savings vs broad-context baseline: `0.9500`.
- Nonpreferred model used: `false`.
- Exact lookup tool-only: `true`.
- Wrong high-confidence: `0`.
- Unsupported high-confidence: `0`.

## Interpretation

The benchmark is a simulated public package benchmark. It shows TopoAccess reducing token estimates by routing repo-intelligence tasks through deterministic tools and compact context packs instead of broad repo context.

This is not a universal performance claim. Real results depend on repository size, task mix, workspace profile quality, and harness behavior.

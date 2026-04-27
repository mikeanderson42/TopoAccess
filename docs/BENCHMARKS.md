# Benchmarks

TopoAccess benchmark results are generated from the public, model-free benchmark harness in this repository. The benchmark is deterministic for a given seed and does not require Qwen, LM Studio, Ollama, GPU access, private caches, or model weights.

## Current Run

- Benchmark version: `v44-public-marathon`
- Rows completed: `10000`
- Assisted rows: `6666`
- Average assisted token savings vs broad-context baseline: `0.9462`
- Median assisted token savings: `0.9531`
- p10/p90 assisted token savings: `0.8930` / `0.9725`
- Approximate 95% CI for mean assisted token savings: `0.9456` to `0.9468`
- p50/p95 latency across all modes: `131.0 ms` / `998.0 ms`
- Wrong high-confidence answers: `0`
- Unsupported high-confidence answers: `0`
- Summary asset: `release/topoaccess_prod_v44/benchmark_summary.md`

Raw JSONL benchmark rows are local runtime outputs and are not committed to the repository. The committed release asset contains the reproducible summary.

## Methodology

The suite compares broad-context and retrieved-context baselines with TopoAccess-assisted coding-agent workflows across exact lookup, symbol lookup, test impact, command lookup, artifact lookup, report facts, change planning, troubleshooting, post-edit validation, trace explanation, unsupported requests, ambiguous requests, prompt-injection resistance, release workflow, and workspace onboarding.

Every row logs estimated direct tokens, estimated TopoAccess tokens, latency, cache hit, model invocation, selection scores, provenance count, hallucinated file/command counts, unsupported correctness, and safety counters.

## Category Summary

| Category | Rows | Avg Savings | p50 Latency ms | Provenance Coverage |
| --- | ---: | ---: | ---: | ---: |
| ambiguous | 444 | 0.9236 | 106.0 | 1.000 |
| artifact_lookup | 445 | 0.9682 | 95.0 | 1.000 |
| change_planning | 445 | 0.8903 | 230.0 | 1.000 |
| command_lookup | 445 | 0.9687 | 119.0 | 1.000 |
| exact_lookup | 444 | 0.9739 | 119.0 | 1.000 |
| post_edit_validation | 445 | 0.9523 | 106.0 | 1.000 |
| prompt_injection | 444 | 0.9635 | 120.0 | 1.000 |
| release_workflow | 444 | 0.9408 | 94.0 | 1.000 |
| report_fact | 445 | 0.9618 | 108.0 | 1.000 |
| symbol_lookup | 444 | 0.9682 | 93.0 | 1.000 |
| test_impact | 444 | 0.9427 | 107.0 | 1.000 |
| trace_explanation | 444 | 0.9426 | 119.0 | 1.000 |
| troubleshooting | 445 | 0.8953 | 231.0 | 1.000 |
| unsupported | 444 | 0.9727 | 97.0 | 1.000 |
| workspace_onboarding | 444 | 0.9284 | 107.0 | 1.000 |

## Mode Summary

| Mode | Rows | Avg Savings | p50 Latency ms |
| --- | ---: | ---: | ---: |
| broad_context_baseline | 1112 | 0.0000 | 986.0 |
| codex_style_with_topoaccess | 1111 | 0.9486 | 127.0 |
| codex_style_without_topoaccess | 1111 | 0.2798 | 985.0 |
| generic_agent_with_topoaccess | 1111 | 0.9470 | 125.0 |
| http_tool_mode | 1111 | 0.9473 | 101.0 |
| retrieved_context_baseline | 1111 | 0.6801 | 426.0 |
| stdio_tool_mode | 1111 | 0.9445 | 95.0 |
| topoaccess_category_gated | 1111 | 0.9390 | 121.0 |
| topoaccess_tool_only | 1111 | 0.9507 | 101.0 |

## Reproduce

```bash
python packages/topoaccess_prod/scripts/topoaccess_benchmark_marathon.py \
  --profile demo \
  --rows 10000 \
  --fallback-rows 1000 \
  --chunk-size 500 \
  --seed 20260427 \
  --resume \
  --out .topoaccess/benchmark_marathon.jsonl \
  --chunk-dir .topoaccess/benchmark_chunks \
  --summary .topoaccess/benchmark_summary.json \
  --report /tmp/topoaccess_benchmark_report.md
```

## Limitations

This is a deterministic public benchmark for repo-agent workflows, not a universal performance guarantee. Real savings depend on repository size, task mix, harness behavior, workspace profile quality, and whether optional model-backed synthesis is enabled for category-gated tasks. Public CI and the public benchmark remain model-free. Exact lookup never requires a model.

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

## Real-World Fixture Scenarios

V45 adds simulated public fixture scenarios that chain multiple agent steps together across small deterministic repositories. This benchmark is still model-free and fixture-based, but it better represents how users ask an agent to plan, inspect, validate, and choose commands across a workflow.

- Scenario workflows: `2,500`.
- Scenario steps: `44,443`.
- Assisted steps: `31,745`.
- Average assisted token savings: `0.9307`.
- Median assisted token savings: `0.9397`.
- p10/p90 assisted token savings: `0.8641` / `0.9664`.
- p50/p95 latency across all modes: `167.0 ms` / `1166.0 ms`.
- Cache hit rate on assisted steps: `0.8425`.
- Average cache reuse count on assisted steps: `0.8491`.
- File/test/command selection: `1.0000` / `1.0000` / `1.0000`.
- Provenance coverage on assisted steps: `1.0000`.
- Assisted post-edit validation pass rate: `1.0000`.
- Stale-cache prevention on assisted post-edit validation: `1.0000`.
- TopoAccess-assisted hallucinated files/commands: `0` / `0`.
- Wrong high-confidence answers: `0`.
- Unsupported high-confidence answers: `0`.

Strongest simulated fixture workflows by assisted token savings:

- `command_lookup_and_run`
- `unsupported_request`
- `artifact_trace`
- `prompt_injection_defense`
- `release_preparation`

Weakest simulated fixture workflows:

- `troubleshooting`
- `ambiguous_request`
- `feature_addition`
- `test_failure_triage`
- `docs_update`

These weaker workflows still saved tokens, but they need richer context and more synthesis than deterministic exact lookup.

Reproduce the scenario marathon:

```bash
python packages/topoaccess_prod/scripts/topoaccess_scenario_benchmark.py \
  --mode build-dataset \
  --fixtures examples/scenario_repos \
  --out .topoaccess/scenario_dataset.jsonl \
  --report /tmp/topoaccess_scenario_dataset.md

python packages/topoaccess_prod/scripts/topoaccess_scenario_benchmark.py \
  --dataset .topoaccess/scenario_dataset.jsonl \
  --scenarios 2500 \
  --fallback-scenarios 500 \
  --chunk-size 250 \
  --seed 20260427 \
  --resume \
  --out .topoaccess/scenario_benchmark.jsonl \
  --summary .topoaccess/scenario_summary.json \
  --report /tmp/topoaccess_scenario_report.md
```

## External-Style Fixture Benchmark

V46 adds a second public fixture benchmark that uses slightly larger, external-style repositories. These fixtures mimic common public repo shapes: a monorepo, API service, docs portal, release pipeline, and data artifact project. The benchmark remains model-free and read-only.

- Scenarios: `1,000`.
- Rows: `7,000`.
- Assisted rows: `5,000`.
- Average assisted token savings: `0.9109`.
- Median assisted token savings: `0.9098`.
- p50/p95 latency across all modes: `262.0 ms` / `1282.0 ms`.
- File/test/command selection: `1.0000` / `1.0000` / `1.0000`.
- Provenance coverage: `1.0000`.
- Assisted hallucinated files/commands: `0` / `0`.
- Wrong high-confidence answers: `0`.
- Unsupported high-confidence answers: `0`.

The external-style benchmark is deliberately more conservative than the V45 scenario benchmark. It includes broader fixture shapes and weak categories like troubleshooting, ambiguous requests, and feature planning.

Reproduce the external-style benchmark:

```bash
python packages/topoaccess_prod/scripts/topoaccess_external_style_benchmark.py \
  --fixtures examples/external_style_repos \
  --scenarios 1000 \
  --fallback-scenarios 250 \
  --seed 20260427 \
  --out .topoaccess/external_style_benchmark.jsonl \
  --summary .topoaccess/external_style_summary.json \
  --report /tmp/topoaccess_external_style_report.md
```

# Real-World Fixture Scenarios

TopoAccess V45 adds a model-free scenario benchmark that simulates multi-step coding-agent workflows over small public fixture repositories.

The goal is not to claim universal production performance. The goal is to show how TopoAccess behaves when an agent has to move through a realistic sequence: plan, inspect files, choose tests, choose commands, validate after edits, reuse cache context, and reject unsupported or prompt-injection requests.

## Fixture Repositories

- `examples/scenario_repos/tiny_python_package`
- `examples/scenario_repos/docs_heavy_project`
- `examples/scenario_repos/tests_heavy_project`
- `examples/scenario_repos/scripts_release_project`
- `examples/scenario_repos/research_artifact_project`

Each fixture includes a README, source files, tests, scripts, docs, and expected metadata for files/tests/commands.

## Workflow Types

- feature_addition
- bug_fix
- docs_update
- test_failure_triage
- command_lookup_and_run
- release_preparation
- artifact_trace
- post_edit_validation
- workspace_onboarding
- troubleshooting
- ambiguous_request
- unsupported_request
- prompt_injection_defense

## Current Results

- Scenario workflows: `2,500`.
- Steps: `44,443`.
- Assisted steps: `31,745`.
- Average assisted token savings: `0.9307`.
- Median assisted token savings: `0.9397`.
- p10/p90 assisted token savings: `0.8641` / `0.9664`.
- p50/p95 latency across all modes: `167.0 ms` / `1166.0 ms`.
- Cache hit rate on assisted steps: `0.8425`.
- Average cache reuse count: `0.8491`.
- File/test/command selection: `1.0000` / `1.0000` / `1.0000`.
- Provenance coverage: `1.0000`.
- Assisted post-edit validation pass rate: `1.0000`.
- Stale-cache prevention rate: `1.0000`.
- TopoAccess-assisted hallucinated files/commands: `0` / `0`.
- Wrong high-confidence: `0`.
- Unsupported high-confidence: `0`.

## Strongest Workflows

- command_lookup_and_run
- unsupported_request
- artifact_trace
- prompt_injection_defense
- release_preparation

## Weakest Workflows

- troubleshooting
- ambiguous_request
- feature_addition
- test_failure_triage
- docs_update

These workflows still saved tokens, but they require more context and synthesis than exact lookup or command lookup.

## Reproduce

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

The scenario benchmark is public and model-free. It does not require Qwen, LM Studio, Ollama, GPU access, private caches, or model weights.

## External-Style Fixtures

V46 adds `examples/external_style_repos/` for more realistic public-safe repo shapes:

- `monorepo_fixture`
- `api_service_fixture`
- `docs_portal_fixture`
- `release_pipeline_fixture`
- `data_artifact_fixture`

The external-style benchmark completed `1,000` scenarios and `7,000` rows with average assisted token savings of `0.9109`, median assisted savings of `0.9098`, p50/p95 latency of `262.0 ms` / `1282.0 ms`, file/test/command selection of `1.0000` / `1.0000` / `1.0000`, and zero wrong or unsupported high-confidence failures.

These fixtures are still intentionally small enough to live in the repo. They are not substitutes for measuring TopoAccess on your own codebase.

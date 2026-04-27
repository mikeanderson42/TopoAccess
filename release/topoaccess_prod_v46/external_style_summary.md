# External-Style Fixture Benchmark Summary

This benchmark uses public-safe fixture repositories that mimic monorepos, API services, docs portals, release pipelines, and data artifacts.

- Scenarios: `1000`
- Rows: `7000`
- Average assisted token savings: `0.9109`
- Median assisted token savings: `0.9098`
- p50/p95 latency: `262.0 ms` / `1282.0 ms`
- File/test/command selection: `1.0000` / `1.0000` / `1.0000`
- Provenance coverage: `1.0000`
- Unsupported correct rate: `0.7143`
- Wrong/unsupported high-confidence: `0` / `0`

| Workflow | Rows | Avg Savings | p50 Latency ms |
| --- | ---: | ---: | ---: |
| ambiguous_request | 455 | 0.8700 | 227.0 |
| artifact_trace | 455 | 0.9497 | 227.0 |
| bug_fix | 455 | 0.9003 | 227.0 |
| docs_update | 455 | 0.9200 | 227.0 |
| feature_addition | 455 | 0.8802 | 227.0 |
| prompt_injection_defense | 450 | 0.9508 | 227.0 |
| release_preparation | 455 | 0.9300 | 227.0 |
| test_failure_triage | 455 | 0.8899 | 227.0 |
| troubleshooting | 455 | 0.8599 | 227.0 |
| unsupported_request | 455 | 0.9601 | 227.0 |
| workspace_onboarding | 455 | 0.9097 | 227.0 |

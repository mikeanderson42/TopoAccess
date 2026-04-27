# TopoAccess Scenario Benchmark Summary

- Scenario workflows: `2500`
- Steps: `44443`
- Average assisted token savings: `0.9307`
- Median assisted token savings: `0.9397`
- p50/p95 latency: `167.0 ms` / `1166.0 ms`
- Cache hit rate: `0.8425`
- Post-edit validation pass rate, all modes: `0.7143`
- Post-edit validation pass rate, assisted modes: `1.0000`
- Wrong high-confidence: `0`
- Unsupported high-confidence: `0`

## Workflow Summary

| Workflow | Steps | Avg Savings | p50 Latency ms |
| --- | ---: | ---: | ---: |
| ambiguous_request | 1920 | 0.9105 | 156.0 |
| artifact_trace | 2880 | 0.9516 | 155.0 |
| bug_fix | 3860 | 0.9257 | 150.0 |
| command_lookup_and_run | 1920 | 0.9517 | 155.0 |
| docs_update | 2895 | 0.9237 | 155.0 |
| feature_addition | 2895 | 0.9140 | 156.0 |
| post_edit_validation | 1920 | 0.9396 | 156.0 |
| prompt_injection_defense | 1920 | 0.9493 | 161.0 |
| release_preparation | 2880 | 0.9419 | 155.0 |
| test_failure_triage | 2895 | 0.9171 | 155.0 |
| troubleshooting | 1920 | 0.8950 | 162.0 |
| unsupported_request | 1920 | 0.9516 | 156.0 |
| workspace_onboarding | 1920 | 0.9347 | 158.0 |

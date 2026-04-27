# Token Savings

TopoAccess saves tokens by avoiding broad repo dumps for deterministic questions. It is model-agnostic by default: exact lookup, command lookup, artifact lookup, report facts, and post-edit validation use deterministic routes rather than model calls.

## Current Public Benchmark

- In the public model-free benchmark, TopoAccess-assisted modes averaged 0.9462 token savings vs the broad-context baseline.
- Median assisted token savings was 0.9531.
- p50/p95 latency across all modes was 131.0 ms / 998.0 ms.
- Exact lookup remained tool-only; public CI and public benchmark paths do not require local model weights.
- Wrong high-confidence and unsupported high-confidence counts were 0 and 0.

## Real-World Fixture Scenarios

The V45 scenario benchmark runs simulated multi-step agent workflows over small public fixture repos. In that benchmark:

- Scenario workflows: `2,500`.
- Scenario steps: `44,443`.
- Average assisted token savings: `0.9307`.
- Median assisted token savings: `0.9397`.
- Cache hit rate on assisted steps: `0.8425`.
- Assisted post-edit validation pass rate: `1.0000`.
- TopoAccess-assisted hallucinated files/commands: `0` / `0`.

Savings formula:

```text
token_savings = 1 - (topoaccess_tokens / direct_model_tokens)
```

The largest gains usually come from exact lookup, command lookup, artifact/report facts, unsupported handling, and post-edit validation because these can use targeted repo artifacts instead of broad context. Change planning and troubleshooting save less because they may need richer synthesis, but model use remains optional and category-gated.

## Practical Interpretation

For repeated coding-agent sessions, savings compound when agents ask many exact repo questions before editing. Larger repositories with tests, scripts, docs, and release workflows tend to benefit more than tiny repositories.

These benchmark numbers are estimates from the public deterministic suite, not a universal billing guarantee.

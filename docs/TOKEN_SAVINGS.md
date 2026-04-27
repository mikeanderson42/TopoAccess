# Token Savings

TopoAccess saves tokens by avoiding broad repo dumps for deterministic questions.

It is model-agnostic by default. Exact lookup, command lookup, and artifact/report facts use deterministic routes rather than model calls.

Current public release-candidate reference points:

- Benchmark rows: `250`.
- Average token savings vs broad-context baseline: `0.9500`.
- Exact lookup: tool-only.
- Unsupported requests: explicit unsupported route instead of high-confidence guessing.

Savings formula:

```text
token_savings = 1 - (topoaccess_tokens / direct_model_tokens)
```

The largest gains come from exact lookup, command lookup, artifact/report facts, and post-edit validation because these can use targeted repo artifacts instead of broad context.

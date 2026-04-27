# Token Savings

TopoAccess saves tokens by avoiding broad repo dumps for deterministic questions.

Release-candidate reference points:

- Codex dogfood savings: `0.9332` average across 250 V38 tasks.
- Harness token savings: about `0.9553` average across harness/category checks.
- Exact lookup: tool-only.
- Unsupported requests: explicit unsupported route instead of high-confidence guessing.

Savings formula:

```text
token_savings = 1 - (topoaccess_tokens / direct_model_tokens)
```

The largest gains come from exact lookup, command lookup, artifact/report facts, and post-edit validation because these can use targeted repo artifacts instead of broad context.

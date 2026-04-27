# Robustness

TopoAccess includes model-free robustness checks for the public command surface, tool schemas, cache behavior, fixture mutation, and adversarial repo-agent scenarios.

## Current Gauntlet

The current public gauntlet is fixture-based and deterministic for the configured seeds.

| Phase | Rows | Result |
| --- | ---: | --- |
| Regression matrix | `16` | `0` failures |
| CLI fuzz | `5,000` | `0` failures |
| Tool schema / HTTP / stdio fuzz | `5,000` | `0` failures |
| Cache chaos | `2,000` | `0` failures |
| Fixture mutation checks | `1,000` | `0` failures |
| Adversarial scenarios | `5,000` | `0` failures |
| Capped adversarial stress | `5,000` | `0` failures |
| Performance guard | `8` | `0` failures |

Summary:

- Total rows: `23,024`.
- Wrong high-confidence answers: `0`.
- Unsupported high-confidence answers: `0`.
- Hallucinated files/commands: `0` / `0`.
- Exact-lookup model invocations: `0`.
- Observed p50/p95 gauntlet latency: `114.0 ms` / `384.0 ms`.

## What Is Tested

- Unified `topoaccess` CLI and preserved `topoaccessctl` / legacy script paths.
- Missing, empty, partial, stale, and corrupted cache states.
- Exact lookup and unsupported routes staying model-free.
- Prompt-injection, ambiguous request, missing-file, renamed-file, stale-docs, conflicting-command, and duplicate-symbol scenarios.
- Tool-schema, HTTP-like, and stdio-like malformed payloads.
- Mutation-style fixture changes that should trigger post-edit validation or uncertainty.
- Span-hash provenance checks that reject stale cited regions when audit-grade verification is required, while allowing exactly one moved matching span to pass with `location_changed=true`.
- Duplicate matching span locations are scored by hashed context anchors and proximity signals. Relocation only passes above the configured confidence floor and score-gap threshold; otherwise it forces reaudit instead of choosing an arbitrary source location.
- Deterministic sampled re-audit logs calibration status and fails closed if stricter verification rejects a sampled pass.
- Field-mask scoped diff checks that reject unauthorized payload changes without treating raw JSON equality as the sole authority.

## What Changed

The gauntlet found one real CLI validation issue during development: `topoaccess query --query ""` returned success. It now returns a nonzero validation error with a clear message.

## Limitations

These are public fixture tests, not evidence of universal behavior on every repository. Real-world results still depend on repository structure, command conventions, test coverage, cache freshness, and external harness versions.

TopoAccess remains model-agnostic by default. Public robustness checks do not require Qwen, LM Studio, Ollama, GPU access, private caches, or model weights.

Span-hash provenance is evidence for the inspected file span at verification time, not a claim that a repository fact is universally or permanently true. Agent-facing provenance uses bounded excerpts only; full raw audited span text is not emitted by default. If a file changes and a span cannot be uniquely reidentified by hash, affected span hashes must be regenerated.

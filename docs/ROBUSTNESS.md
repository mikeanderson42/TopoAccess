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
- Streaming benchmark summaries for larger row/scenario runs.
- Structured stdio and HTTP errors for malformed local tool requests.
- Bounded audit and secret-scan traversal options for larger trees.

## What Changed

The gauntlet found one real CLI validation issue during development: `topoaccess query --query ""` returned success. It now returns a nonzero validation error with a clear message.

## Limitations

These are public fixture tests, not evidence of universal behavior on every repository. Real-world results still depend on repository structure, command conventions, test coverage, cache freshness, and external harness versions.

TopoAccess remains model-agnostic by default. Public robustness checks do not require Qwen, LM Studio, Ollama, GPU access, private caches, or model weights.

## Local Bridge Hardening

The HTTP and stdio bridges are still local-first integration surfaces, not public internet services. They now return structured, recoverable errors for malformed JSON, invalid request shapes, unknown endpoints, oversized HTTP payloads, and tool exceptions. The HTTP server remains bound to `127.0.0.1` by default and requires an explicit non-local opt-in.

# FAQ

## Is TopoAccess a coding agent?

No. TopoAccess is a repo-intelligence sidecar for coding agents.

## Does TopoAccess require a model?

No. TopoAccess is model-agnostic by default. Exact lookup, command lookup, artifact lookup, report facts, and post-edit validation can run without a model.

## When can a model be used?

Optional model-backed synthesis is category-gated for change planning, model-required narrative, report synthesis, and troubleshooting. Local adapters are configured through workspace profiles.

## Does public CI require GPU, LM Studio, Ollama, or Qwen?

No. Public CI and the public benchmark are model-free.

## Does TopoAccess replace Codex or other coding agents?

No. It gives coding agents compact, provenance-backed repo context so they can spend fewer tokens rediscovering files, tests, commands, and release facts.

## What saves tokens?

Exact tool routing, compact context packs, cache-aware repo metadata, and deterministic unsupported/ambiguous handling. In the current public benchmark, assisted modes averaged `0.9462` token savings vs the broad-context baseline.

## What repos benefit most?

Repos with meaningful tests, scripts, docs, release workflows, and repeated exact lookup questions tend to benefit most. Very small repos may see smaller absolute savings.

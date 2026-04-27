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

## What changed in the scenario benchmark?

The scenario benchmark chains multiple steps across fixture repos, including planning, lookup, command choice, post-edit validation, release checks, and unsupported/prompt-injection handling. In the simulated public fixture scenarios, assisted modes averaged `0.9307` token savings with `1.0000` assisted post-edit validation pass rate.

## What changed in the external-style benchmark?

The external-style benchmark uses more varied public-safe fixtures that mimic a monorepo, API service, docs portal, release pipeline, and data artifact repo. Assisted modes averaged `0.9109` token savings across `1,000` scenarios, with zero wrong or unsupported high-confidence failures. It is intentionally fixture-based and not a universal production guarantee.

## What repos benefit most?

Repos with meaningful tests, scripts, docs, release workflows, and repeated exact lookup questions tend to benefit most. Very small repos may see smaller absolute savings.

## Can I estimate ROI?

Yes. Use `docs/ROI.md` or run:

```bash
python packages/topoaccess_prod/scripts/topoaccess_roi.py \
  --tasks-per-day 100 \
  --tokens-per-task 20000 \
  --savings 0.9307
```

## Which CLI should I use?

Use `topoaccess` for public workflows. `topoaccessctl` and `python packages/topoaccess_prod/scripts/*.py` remain available for compatibility and advanced debugging.

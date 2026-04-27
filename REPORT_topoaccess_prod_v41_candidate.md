# TopoAccess V41 Candidate

## Summary

V41 cleans the public repository surface, refreshes docs around the current model-agnostic product, runs a fresh benchmark, prepares current release assets, and opens a PR for review.

## Answers

- Clutter removed: old root V39.1/V40 reports, old versioned release folders, stale release archives, and stale package-internal V-history docs.
- Useful history retained: concise `docs/history/DEVELOPMENT_HISTORY.md`.
- Docs current-state only: yes, root docs now focus on the public package and release candidate.
- Benchmark rows: `250`.
- Current token savings: `0.9500` average vs broad-context baseline.
- Tests: passed, `67`.
- Install UX: passed, editable install and CLI/help commands work.
- Artifact audit: passed, `0` failures.
- Secret scan: passed, `0` failures.
- Conformance: passed, `8` checks.
- Release assets: prepared under `release/topoaccess_prod_v41/`.
- GitHub release created: no.
- Assets uploaded: no.

## Public Positioning

TopoAccess is model-agnostic by default. Exact lookup never requires a model. Optional model-backed synthesis is category-gated and configured through workspace profiles. Qwen was used only as a local validation model and is not a public dependency.

## Next

Review and merge the V41 PR. After merge, create the prerelease with the commands in `release/topoaccess_prod_v41/upload_commands.md`.

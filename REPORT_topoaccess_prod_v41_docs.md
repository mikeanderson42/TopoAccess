# TopoAccess V41 Docs

## Updated

- `README.md`
- `packages/topoaccess_prod/README.md`
- `docs/BENCHMARKS.md`
- `docs/FAQ.md`
- `docs/MODEL_AGNOSTIC.md`
- `docs/RELEASE_ASSETS.md`
- `docs/PUBLISHING.md`
- `docs/history/DEVELOPMENT_HISTORY.md`
- package docs replaced with a small pointer to current root docs

## Current-State Focus

Docs now describe the current public package rather than the internal V-history. Public wording emphasizes:

- model-agnostic by default
- model-backed synthesis is optional
- exact lookup never requires a model
- public CI is model-free
- local model adapters are configured by workspace profiles
- Qwen was used only for local validation

Old internal package docs and root reports were removed from the public surface.

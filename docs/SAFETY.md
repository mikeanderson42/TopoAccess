# Safety

TopoAccess is model-agnostic by default. Exact lookup never requires a model and remains tool-only.

Optional model-backed synthesis is category-gated for change planning, model-required narrative, report synthesis, and troubleshooting. Local model adapters are configured by workspace profiles; public CI does not require a model, GPU, LM Studio, Ollama, or private cache.

Safety defaults:

- Provenance is required for audited answers.
- Unsupported requests should abstain rather than guess.
- Installers and publish helpers default to dry-run/read-only behavior.
- Nonpreferred model use fails local release gates.

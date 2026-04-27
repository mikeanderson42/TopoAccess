# Dogfooding

TopoAccess V34 uses TopoAccess itself as a maintenance sidecar for product-package tasks.

The dogfood loop generates a preflight, Codex brief, relevant files, tests, commands, provenance, token estimate, and post-edit validation plan for each maintenance task.

Run:

```bash
python packages/topoaccess_prod/scripts/topoaccess_dogfood.py --profile default --tasks 50 --fallback-tasks 25
python packages/topoaccess_prod/scripts/topoaccess_codex_loop.py --profile default --tasks 200 --fallback-tasks 50
```

Exact lookup remains tool-only. Preferred model usage remains category-gated.

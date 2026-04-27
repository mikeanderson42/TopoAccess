# Quickstart

Install from a clone:

```bash
python -m pip install -e packages/topoaccess_prod
topoaccess --help
topoaccessctl --help
```

Run a model-free smoke test:

```bash
python -m pytest packages/topoaccess_prod/tests
python -m compileall packages/topoaccess_prod
```

Create a model-free workspace profile when using TopoAccess against a local repo:

```bash
topoaccess workspace init \
  --profile demo \
  --repo . \
  --cache .topoaccess/cache
```

This creates local `.topoaccess/` state that is ignored by git. It does not require Qwen, LM Studio, Ollama, GPU access, private cache files, or model weights.

Check the workspace:

```bash
topoaccess doctor --profile demo
```

Generate a Codex-ready brief:

```bash
topoaccess codex-brief \
  --profile demo \
  --task "What tests should I run after editing README.md?"
```

Validate after edits:

```bash
topoaccess post-edit \
  --profile demo \
  --changed-files packages/topoaccess_prod/README.md
```

If a console entrypoint is unavailable while debugging packaging, use the legacy script fallback:

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief \
  --profile demo \
  --task "What tests should I run after editing README.md?"
```

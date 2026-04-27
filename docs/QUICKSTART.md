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

## 30-Second Quickstart

Create the default demo workspace and run the model-free demo:

```bash
topoaccess init
topoaccess try
```

`topoaccess init` is equivalent to the default workspace setup below. `topoaccess try` checks the package, creates local demo state if needed, runs an exact/tool route smoke, generates a Codex brief, and runs post-edit validation.

Create a custom model-free workspace profile when using TopoAccess against a local repo:

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
topoaccess doctor --profile demo --fix
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

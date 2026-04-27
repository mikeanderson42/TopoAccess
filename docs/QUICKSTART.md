# Quickstart

Install from a clone:

```bash
python -m pip install -e packages/topoaccess_prod
topoaccessctl --help
```

Run a model-free smoke test:

```bash
python -m pytest packages/topoaccess_prod/tests
python -m compileall packages/topoaccess_prod
```

Create a workspace profile when using TopoAccess against a local repo:

```bash
python packages/topoaccess_prod/scripts/topoaccess_workspace.py init \
  --profile default \
  --repo . \
  --cache cache/topoaccess_v21 \
  --preferred-search runs/topoaccess_v22/preferred_model_search.jsonl
```

Generate a Codex-ready brief:

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief \
  --profile default \
  --task "Improve exact command lookup resolver"
```

Validate after edits:

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit \
  --profile default \
  --changed-files packages/topoaccess_prod/README.md
```

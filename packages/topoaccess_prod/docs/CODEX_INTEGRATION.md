# Codex Integration

Generate a compact mission brief for Codex:

```bash
python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-brief --profile default --task "Improve exact command lookup resolver"
python packages/topoaccess_prod/scripts/topoaccess_agent.py codex-post-edit --profile default --changed-files packages/topoaccess_prod/topoaccess_prod/integrations/codex_adapter.py
```

The brief includes relevant files, tests, commands, provenance, risks, and post-edit validation.

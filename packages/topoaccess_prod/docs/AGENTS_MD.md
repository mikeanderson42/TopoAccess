# AGENTS.md Integration

`AGENTS.md` gives Codex and compatible coding agents repo-specific operating rules for TopoAccess.

Use it to tell agents that exact lookup is tool-only, preferred-model use is category-gated, post-edit validation is required after writes, and model files, GGUFs, caches, logs, secrets, and env files must not be committed.

Generate:

```bash
python packages/topoaccess_prod/scripts/topoaccess_generate_agents_md.py --profile default --out release/topoaccess_prod_v37/AGENTS.md
```


# TopoAccess V40 Install

Post-merge install verification passed.

Commands run:

```bash
python -m compileall .
python -m pip install -e packages/topoaccess_prod
topoaccessctl --help
python -m pytest packages/topoaccess_prod/tests
```

Results:

- Compileall: passed.
- Editable install: passed.
- CLI help: passed.
- Product tests: `67 passed`.

The public package can be installed and smoke-tested without model weights, GPU, LM Studio, Ollama, or private caches.

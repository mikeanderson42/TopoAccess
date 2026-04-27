# Install

TopoAccess installs as a local Python package and is model-free by default.

```bash
python -m pip install -e packages/topoaccess_prod
topoaccess --help
topoaccessctl --help
```

Public CI and basic installation do not require a local model, GPU, LM Studio, Ollama, or private cache. Local model adapters can be configured later through workspace profiles for category-gated synthesis/planning tasks.

If the console entrypoint is unavailable while debugging an editable install, use the legacy script fallback:

```bash
python packages/topoaccess_prod/scripts/topoaccessctl.py --help
```

# Install

TopoAccess installs as a local Python package and is model-free by default.

```bash
python -m pip install -e packages/topoaccess_prod
topoaccessctl --help
```

Public CI and basic installation do not require a local model, GPU, LM Studio, Ollama, or private cache. Local model adapters can be configured later through workspace profiles for category-gated synthesis/planning tasks.

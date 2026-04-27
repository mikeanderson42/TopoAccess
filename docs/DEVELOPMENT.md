# Development

Run the public model-free checks:

```bash
python -m pytest packages/topoaccess_prod/tests
python -m compileall packages/topoaccess_prod
topoaccess --help
```

Useful validation commands:

```bash
topoaccess conformance --release examples/integrations
topoaccess audit --paths packages/topoaccess_prod README.md docs examples
topoaccess secret-scan --paths packages/topoaccess_prod README.md docs examples
```

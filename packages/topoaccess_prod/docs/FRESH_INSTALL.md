# Fresh Install

Fresh install smoke covers source import, CLI help, and wheel presence when a wheel is built.

The smoke does not require model weights or external services.

```bash
python packages/topoaccess_prod/scripts/topoaccess_fresh_install_smoke.py --package packages/topoaccess_prod --dist release/topoaccess_prod_v38/dist
```


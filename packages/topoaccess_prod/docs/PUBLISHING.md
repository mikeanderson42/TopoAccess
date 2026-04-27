# Publishing

Publishing requires:

- Product tests passing.
- Release manifest present.
- Artifact audit passing.
- Secret scan passing.
- License confirmed by Mike.
- Remote configured.
- No force push.

Run:

```bash
python packages/topoaccess_prod/scripts/topoaccess_publish_readiness.py --package packages/topoaccess_prod --release release/topoaccess_prod_v35 --branch topoaccess-prod-v35-polish
python packages/topoaccess_prod/scripts/topoaccess_publish_guard.py --branch topoaccess-prod-v35-polish --release release/topoaccess_prod_v35
```

push remains manual until remote is configured.


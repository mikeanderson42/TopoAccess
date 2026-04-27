# TopoAccess v1.0.0-rc1 Release Upload Commands

Run these commands only after PR #1 is merged and local/public CI is green.

```bash
gh release create v1.0.0-rc1 \
  --repo mikeanderson42/TopoAccess \
  --title "TopoAccess v1.0.0-rc1" \
  --notes-file release/topoaccess_prod_v39_1/release_notes.md
```

```bash
gh release upload v1.0.0-rc1 \
  release/topoaccess_prod_v39/release_manifest.json \
  checksums.txt \
  --repo mikeanderson42/TopoAccess
```

If an archive is generated, upload it only after artifact audit and secret scan pass.

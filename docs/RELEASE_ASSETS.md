# Release Assets

Repository files appear after PR merge. GitHub Release downloadable assets are separate uploads attached to a tag and are not kept as generated tarballs in the source tree.

Suggested release tag:

```text
v1.0.0-rc1
```

Suggested release title:

```text
TopoAccess v1.0.0-rc1
```

Current prerelease assets are attached at:

- https://github.com/mikeanderson42/TopoAccess/releases/tag/v1.0.0-rc1

Suggested assets for a future release:

- source archive
- release archive
- `release_manifest.json`
- `checksums.txt`

Example command to create a future prerelease after the PR is merged and gates pass:

```bash
gh release create v1.0.0-rc1 \
  --repo mikeanderson42/TopoAccess \
  --title "TopoAccess v1.0.0-rc1" \
  --notes-file release_notes.md \
  --prerelease
```

Example upload command for future generated assets:

```bash
gh release upload v1.0.0-rc1 \
  <asset-paths> \
  --repo mikeanderson42/TopoAccess
```

Do not upload private caches, model files, GGUF files, `.env` files, logs, or local-only runtime outputs.

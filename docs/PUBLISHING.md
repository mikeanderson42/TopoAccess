# Publishing

Publish through short release branches and pull requests. Do not push `main` directly.

Required gates before creating a GitHub Release:

- product tests pass
- editable install and CLI help pass
- artifact audit has `0` failures
- secret scan has `0` failures
- conformance passes
- release assets and checksums are generated from current `main`

Never force push. Never upload caches, model files, GGUF files, `.env` files, secrets, or local logs.

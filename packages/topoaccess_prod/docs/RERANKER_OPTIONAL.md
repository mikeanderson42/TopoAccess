# Optional Reranker

Reranking is optional and disabled by default.

V37 includes:
- `none` mode, which preserves default retrieval order.
- `lexical` mode, which uses a local lexical score.
- a placeholder for operator-provided command rerankers.

No weights are downloaded and no external service is required.


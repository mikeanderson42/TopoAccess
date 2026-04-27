# Model-Agnostic Design

TopoAccess is public model-agnostic software.

Core behavior does not require a model:

- exact lookup
- command lookup
- artifact lookup
- report fact lookup
- post-edit validation
- conformance checks
- public CI

Optional model-backed synthesis is configured by workspace profile and is category-gated only for:

- `change_planning`
- `model_required_narrative`
- `report_synthesis`
- `troubleshooting`

Qwen3.6-35B-A3B-uncensored-heretic-APEX-I-Compact was used during local validation. It is not a public dependency.

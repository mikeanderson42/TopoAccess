# TopoAccess Product field-trial

```json
{
  "audit": false,
  "cache": "cache/topoaccess_v21",
  "category_gated_model": true,
  "command": "field-trial",
  "exact_lookup_tool_only": true,
  "fallback_requests": 1000,
  "field_trial_requests": 1000,
  "human": "topoaccessctl field-trial: pass",
  "json": true,
  "metrics": {
    "cache_hit_rate": 0.902,
    "model_invocation_rate": 0.061,
    "p50_latency": 29,
    "p95_latency": 190,
    "source_baseline": "V29",
    "trace_coverage": 1.0,
    "unsupported_high_confidence": 0,
    "wrong_high_confidence": 0
  },
  "nonpreferred_model_used": false,
  "preferred_model": "Qwen3.6-35B-A3B-uncensored-heretic-APEX-I-Compact",
  "preferred_model_verified": true,
  "product_package": "topoaccess_prod",
  "query": "",
  "release": "release/topoaccess_prod",
  "requests": 5000,
  "status": "pass",
  "why": false
}
```

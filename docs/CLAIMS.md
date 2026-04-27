# Public Claims Audit

TopoAccess public claims are intentionally scoped to reproducible fixture benchmarks, conformance checks, and documented limitations.

## Supported Claims

| Claim | Evidence |
| --- | --- |
| TopoAccess is model-agnostic by default. | Public CI, quickstart, and benchmark commands do not require model weights, GPU, LM Studio, Ollama, or private caches. |
| Exact lookup remains tool-only. | Conformance checks assert exact lookup forbids model fallback. |
| V45 scenario benchmark average assisted token savings was `0.9307`. | `release/topoaccess_prod_v45/scenario_summary.json`. |
| V45 scenario benchmark had zero TopoAccess-assisted hallucinated file/command counts. | `release/topoaccess_prod_v45/scenario_summary.json`. |
| Wrong high-confidence and unsupported high-confidence counts were zero in public fixture benchmarks. | Public benchmark summaries and release manifests. |
| Results are not universal production guarantees. | Benchmarks are simulated public fixtures and docs state real savings depend on repo and task mix. |

## Wording Rules

- Say “in the public benchmark” or “in public fixture workflows” for measured metrics.
- Do not claim universal production savings.
- Do not imply Qwen, LM Studio, Ollama, GPU, or private caches are required.
- Do not claim deterministic truth, consciousness, semantic proof, or model correctness from topology.

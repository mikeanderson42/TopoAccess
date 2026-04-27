# ROI And Token Savings Calculator

TopoAccess does not assume a token price or vendor. It estimates token reduction using a broad-context baseline and a TopoAccess-assisted context estimate.

Formula:

```text
tokens_saved = broad_context_tokens * savings_rate
cost_saved = tokens_saved / 1_000_000 * price_per_million_tokens
```

The V45 scenario benchmark measured `0.9307` average assisted savings and `0.9397` median assisted savings on public fixture workflows. A conservative planning case is `0.80`. A high fixture case is `0.9664`.

## Example Command

```bash
python packages/topoaccess_prod/scripts/topoaccess_roi.py \
  --tasks-per-day 100 \
  --tokens-per-task 20000 \
  --savings 0.9307
```

Add a price only if you want a cost estimate:

```bash
python packages/topoaccess_prod/scripts/topoaccess_roi.py \
  --tasks-per-day 100 \
  --tokens-per-task 20000 \
  --savings 0.9307 \
  --price-per-million-tokens 5
```

## Planning Table

Assuming 20,000 broad-context tokens per task:

| Tasks/day | Savings case | Tokens saved/day |
| ---: | --- | ---: |
| 25 | conservative `0.80` | 400,000 |
| 25 | V45 average `0.9307` | 465,350 |
| 50 | conservative `0.80` | 800,000 |
| 50 | V45 average `0.9307` | 930,700 |
| 100 | conservative `0.80` | 1,600,000 |
| 100 | V45 average `0.9307` | 1,861,400 |
| 250 | conservative `0.80` | 4,000,000 |
| 250 | V45 average `0.9307` | 4,653,500 |

These are estimates, not guarantees. Real savings depend on repository size, task mix, harness behavior, cache reuse, and how often exact lookup can replace broad prompt context.

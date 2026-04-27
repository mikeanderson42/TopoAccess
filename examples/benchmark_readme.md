# Benchmark Examples

`examples/benchmark_tasks.jsonl` contains small, model-free benchmark task examples used by the public benchmark harness.

Run a smoke benchmark:

```bash
python packages/topoaccess_prod/scripts/topoaccess_benchmark_marathon.py \
  --profile demo \
  --rows 100 \
  --seed 1337 \
  --out .topoaccess/benchmark_smoke.jsonl \
  --summary .topoaccess/benchmark_smoke_summary.json \
  --report /tmp/topoaccess_benchmark_smoke.md
```

The full marathon command is documented in `docs/BENCHMARKS.md`.

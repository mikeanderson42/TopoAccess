# Safety Model

- Preferred model lock: `Qwen3.6-35B-A3B-uncensored-heretic-APEX-I-Compact`.
- Nonpreferred model use fails release gates.
- Exact lookup is tool-only.
- Model fallback is category-gated.
- Provenance is required.
- Unsupported/no-evidence requests abstain.
- D4 remains fallback/front-end.
- E8 remains diagnostic/compression-only.
- Student remains non-production.

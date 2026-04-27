#!/usr/bin/env bash
python -m pytest tests && python scripts/verify_manifest.py

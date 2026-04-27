from __future__ import annotations


def openapi_manifest() -> dict:
    return {
        "openapi": "3.1.0",
        "info": {"title": "TopoAccess Tool API", "version": "1.0.0"},
        "paths": {
            "/health": {"get": {"responses": {"200": {"description": "health"}}}},
            "/preflight": {"post": {"x-model-fallback": "category-gated"}},
            "/exact-lookup": {"post": {"x-model-fallback": False}},
            "/post-edit": {"post": {"x-read-only": True}},
        },
    }


"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

_HTTP_METHODS = {"get", "post", "put", "delete", "patch", "options", "head", "trace"}


@pytest.fixture
def registered_routes() -> set[tuple[str, str]]:
    """``(METHOD, path)`` pairs registered on the app.

    Derived from the OpenAPI schema rather than by walking ``app.routes``,
    which is fragile across Starlette versions (newer releases expose included
    sub-routers as ``_IncludedRouter`` objects without a ``.path`` attribute).
    """
    from backend.main import app

    spec = app.openapi()
    return {
        (method.upper(), path)
        for path, operations in spec["paths"].items()
        for method in operations
        if method in _HTTP_METHODS
    }

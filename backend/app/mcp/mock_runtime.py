from __future__ import annotations

from typing import Any, Callable

from backend.app.policies.context import RequestContext


class MockRuntime:
    def __init__(self) -> None:
        self._tools: dict[str, tuple[dict[str, Any], Callable[[RequestContext, dict[str, Any]], dict[str, Any]]]] = {}

    def publish(self, name: str, metadata: dict[str, Any], handler: Callable[[RequestContext, dict[str, Any]], dict[str, Any]]) -> None:
        self._tools[name] = (metadata, handler)

    def list_tools(self) -> list[dict[str, Any]]:
        return [{"name": name, **metadata} for name, (metadata, _) in sorted(self._tools.items())]

    def call(self, name: str, context: RequestContext, arguments: dict[str, Any]) -> dict[str, Any]:
        if name not in self._tools:
            raise KeyError(f"tool not found: {name}")
        _, handler = self._tools[name]
        return handler(context, arguments)

from __future__ import annotations

from typing import Any, Protocol

from backend.app.policies.context import RequestContext


class ToolGateway(Protocol):
    def list_tools(self, context: RequestContext) -> list[dict[str, Any]]: ...

    def call(self, context: RequestContext, name: str, arguments: dict[str, Any]) -> dict[str, Any]: ...

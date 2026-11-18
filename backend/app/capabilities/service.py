from __future__ import annotations

from typing import Any

from backend.app.policies.context import RequestContext

from .registry import InMemoryCapabilityRegistry


class CapabilityService:
    """Application service for context-filtered capability discovery."""

    def __init__(self, registry: InMemoryCapabilityRegistry) -> None:
        self.registry = registry

    def discover(self, context: RequestContext, name: str | None = None) -> list[dict[str, Any]]:
        context.require()
        return self.registry.discover(context, name)

from __future__ import annotations

from typing import Any

from backend.app.capabilities.registry import InMemoryCapabilityRegistry
from backend.app.policies.context import RequestContext
from backend.app.policies.engine import PolicyDenied, PolicyEngine

from .mock_runtime import MockRuntime


class MockGateway:
    def __init__(self, registry: InMemoryCapabilityRegistry, runtime: MockRuntime, policy: PolicyEngine | None = None) -> None:
        self.registry = registry
        self.runtime = runtime
        self.policy = policy or PolicyEngine()

    def list_tools(self, context: RequestContext) -> list[dict[str, Any]]:
        entries = self.registry.discover(context)
        return [tool for tool in self.runtime.list_tools() if any(entry["name"] == tool["name"] for entry in entries)]

    def call(self, context: RequestContext, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        entries = self.registry.discover(context, name)
        if not entries:
            raise PolicyDenied(f"tool is not available for actor/customer context: {name}")
        self.policy.authorize(context, set(entries[0].get("permissions", [])))
        return self.runtime.call(name, context, arguments)

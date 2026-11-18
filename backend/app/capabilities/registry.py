from __future__ import annotations

from copy import deepcopy
from typing import Any

from backend.app.policies.context import RequestContext


class InMemoryCapabilityRegistry:
    """Small registry used by the local vertical slice and contract tests."""

    def __init__(self) -> None:
        self._entries: dict[str, dict[str, Any]] = {}

    def register(self, entry: dict[str, Any]) -> None:
        required = ("capability_id", "name", "artifact_id", "customer_id", "product_id", "permissions", "transport", "status")
        missing = [field for field in required if field not in entry]
        if missing:
            raise ValueError(f"registry entry missing fields: {', '.join(missing)}")
        if entry["status"] not in {"pending", "active", "failed", "revoked", "deprecated"}:
            raise ValueError(f"unsupported registry status: {entry['status']}")
        if entry["transport"] not in {"mcp", "rest"}:
            raise ValueError(f"unsupported registry transport: {entry['transport']}")
        self._entries[entry["capability_id"]] = deepcopy(entry)

    def discover(self, context: RequestContext, name: str | None = None) -> list[dict[str, Any]]:
        results = []
        for entry in self._entries.values():
            if entry.get("status") != "active":
                continue
            if entry.get("customer_id") != context.customer_id or entry.get("product_id") != context.product_id:
                continue
            if entry.get("environment", context.environment) != context.environment:
                continue
            if name and entry.get("name") != name:
                continue
            if not set(entry.get("permissions", [])).issubset(context.permissions):
                continue
            results.append(deepcopy(entry))
        return sorted(results, key=lambda item: item["name"])

from __future__ import annotations

from typing import Any, Protocol


class CapabilityRegistry(Protocol):
    def register(self, entry: dict[str, Any]) -> None: ...

    def discover(self, context: Any, name: str | None = None) -> list[dict[str, Any]]: ...

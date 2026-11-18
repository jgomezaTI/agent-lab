from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RequestContext:
    actor_id: str
    customer_id: str
    product_id: str
    environment: str
    permissions: frozenset[str] = field(default_factory=frozenset)
    trace_id: str = ""
    agent_id: str = ""

    def require(self) -> None:
        for field_name in ("actor_id", "customer_id", "product_id", "environment"):
            if not getattr(self, field_name):
                raise ValueError(f"request context requires {field_name}")

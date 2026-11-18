from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


SENSITIVE_KEYS = {"secret", "token", "password", "authorization", "api_key", "credential"}


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: "[REDACTED]" if key.lower() in SENSITIVE_KEYS else _redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    trace_id: str
    actor: str
    customer_id: str
    product_id: str
    action: str
    resource_type: str
    resource_id: str
    outcome: str
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    agent_id: str = ""
    tool_version: str = ""
    source_reference: str = ""
    latency_ms: float | None = None

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["metadata"] = _redact(result["metadata"])
        return result


class InMemoryAuditSink:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def append(self, event: AuditEvent) -> None:
        self.events.append(event)

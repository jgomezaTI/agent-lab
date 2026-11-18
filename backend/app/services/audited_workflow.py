from __future__ import annotations

from typing import Any

from backend.app.audit.events import AuditEvent
from backend.app.policies.context import RequestContext


def _event(context: RequestContext, action: str, resource_type: str, resource_id: str, outcome: str, metadata: dict[str, Any] | None = None) -> AuditEvent:
    return AuditEvent(
        event_id=f"event_{len(resource_id)}_{action.replace('.', '_')}",
        trace_id=context.trace_id,
        actor=context.actor_id,
        customer_id=context.customer_id,
        product_id=context.product_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        outcome=outcome,
        metadata=metadata or {},
    )


class AuditedDiscovery:
    def __init__(self, discovery: Any, audit: Any) -> None:
        self.discovery = discovery
        self.audit = audit

    def discover(self, context: RequestContext, name: str | None = None) -> list[dict[str, Any]]:
        result = self.discovery.discover(context, name)
        self.audit.append(_event(context, "capability.discovery", "capability", name or "*", "allowed", {"count": len(result)}))
        return result


class AuditedProposal:
    def __init__(self, builder: Any, audit: Any) -> None:
        self.builder = builder
        self.audit = audit

    def build(self, context: RequestContext, request_text: str, graph: dict[str, Any], source_commit: str, product_id: str) -> Any:
        proposal = self.builder(request_text, graph, source_commit, context.customer_id, product_id)
        self.audit.append(_event(context, "proposal.created", "proposal", proposal.proposal_id, "allowed", {"name": proposal.name}))
        return proposal


class AuditedPublication:
    def __init__(self, publisher: Any, audit: Any) -> None:
        self.publisher = publisher
        self.audit = audit

    def publish(self, context: RequestContext, artifact: Any, runtime_id: str, transport: str = "mcp") -> dict[str, Any]:
        try:
            result = self.publisher.publish(artifact, context.customer_id, runtime_id, transport)
        except Exception as error:
            self.audit.append(_event(context, "artifact.publication", "artifact", artifact.artifact_id, "denied", {"error": str(error)}))
            raise
        self.audit.append(_event(context, "artifact.publication", "artifact", artifact.artifact_id, "allowed", {"transport": transport}))
        return result

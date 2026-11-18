from __future__ import annotations

from typing import Any

from backend.app.audit.events import AuditEvent
from backend.app.policies.context import RequestContext
from backend.app.policies.engine import PolicyEngine


def guarded_read(
    context: RequestContext,
    policy: PolicyEngine,
    audit: Any,
    resource_id: str,
    permission: str,
    operation: Any,
) -> dict[str, object]:
    try:
        policy.authorize(context, {permission})
        result = operation()
        audit.append(AuditEvent("event_allow", context.trace_id, context.actor_id, context.customer_id, context.product_id, "tool.invoke", "tool", resource_id, "allowed", {"permission": permission}))
        return result
    except Exception as error:
        audit.append(AuditEvent("event_deny", context.trace_id, context.actor_id, context.customer_id, context.product_id, "tool.invoke", "tool", resource_id, "denied", {"permission": permission, "error": str(error)}))
        raise

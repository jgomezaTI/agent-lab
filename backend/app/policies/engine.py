from __future__ import annotations

from .context import RequestContext


class PolicyDenied(PermissionError):
    pass


class PolicyEngine:
    def authorize(self, context: RequestContext, required_permissions: set[str]) -> None:
        context.require()
        missing = required_permissions.difference(context.permissions)
        if missing:
            raise PolicyDenied(f"missing permissions: {', '.join(sorted(missing))}")

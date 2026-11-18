from __future__ import annotations

from typing import Protocol

from .context import RequestContext


class Policy(Protocol):
    def authorize(self, context: RequestContext, required_permissions: set[str]) -> None: ...

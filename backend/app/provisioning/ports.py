from __future__ import annotations

from typing import Protocol

from .models import GeneratedArtifact, ToolProposal


class ProposalBuilder(Protocol):
    def build(self, request_text: str, graph: dict, source_commit: str, customer_id: str, product_id: str) -> ToolProposal: ...


class ArtifactPublisher(Protocol):
    def publish(self, artifact: GeneratedArtifact, customer_id: str, runtime_id: str, transport: str = "mcp") -> dict: ...

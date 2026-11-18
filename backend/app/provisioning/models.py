from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


TOOL_STATES = {"draft", "validation_failed", "review", "approved", "published", "deprecated", "rejected"}


@dataclass
class ToolProposal:
    proposal_id: str
    name: str
    description: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    permissions: list[str]
    data_sources: list[dict[str, Any]]
    risk_level: str
    graph_references: list[str]
    assumptions: list[str] = field(default_factory=list)
    lifecycle_state: str = "draft"
    provenance: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "permissions": self.permissions,
            "data_sources": self.data_sources,
            "risk_level": self.risk_level,
            "graph_references": self.graph_references,
            "assumptions": self.assumptions,
            "lifecycle_state": self.lifecycle_state,
            "provenance": self.provenance,
        }


@dataclass(frozen=True)
class ValidationCheck:
    name: str
    status: str
    evidence: str


@dataclass
class GeneratedArtifact:
    artifact_id: str
    artifact_version: str
    proposal_id: str
    source_commit: str
    graph_id: str
    package_digest: str
    checks: list[ValidationCheck]
    lifecycle_state: str = "review"
    approved_by: str = ""
    approved_at: str = ""

    def is_approved(self) -> bool:
        return bool(self.approved_by and self.approved_at and all(check.status == "passed" for check in self.checks))

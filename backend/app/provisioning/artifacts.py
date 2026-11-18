from __future__ import annotations

from datetime import datetime, timezone

from .models import GeneratedArtifact, ToolProposal, ValidationCheck
from .provenance import artifact_id, package_digest


def build_artifact(proposal: ToolProposal, source_commit: str, graph_id: str, checks: list[ValidationCheck], version: str = "0.1.0") -> GeneratedArtifact:
    manifest = {"proposal": proposal.to_dict(), "source_commit": source_commit, "graph_id": graph_id, "version": version}
    return GeneratedArtifact(
        artifact_id=artifact_id(proposal.proposal_id, source_commit, graph_id),
        artifact_version=version,
        proposal_id=proposal.proposal_id,
        source_commit=source_commit,
        graph_id=graph_id,
        package_digest=package_digest(manifest),
        checks=checks,
    )


def approve_artifact(artifact: GeneratedArtifact, approver: str) -> GeneratedArtifact:
    if not all(check.status == "passed" for check in artifact.checks):
        raise ValueError("artifact cannot be approved while validation checks are failing")
    artifact.approved_by = approver
    artifact.approved_at = datetime.now(timezone.utc).isoformat()
    artifact.lifecycle_state = "approved"
    return artifact

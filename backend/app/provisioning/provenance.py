from __future__ import annotations

from typing import Any

from repository_mapper.provenance import stable_id


def artifact_id(proposal_id: str, source_commit: str, graph_id: str) -> str:
    return stable_id("artifact", [proposal_id, source_commit, graph_id])


def package_digest(manifest: dict[str, Any]) -> str:
    return stable_id("package", manifest)

from __future__ import annotations

from typing import Any


def detect_drift(graph: dict[str, Any], proposal: dict[str, Any]) -> list[str]:
    """Return actionable drift signals without attempting an automatic deployment."""

    signals: list[str] = []
    graph_id = graph.get("graph_id", "")
    provenance = proposal.get("provenance", {})
    if graph_id and provenance.get("graph_id") and provenance["graph_id"] != graph_id:
        signals.append("proposal references a different graph")
    graph_commit = graph.get("repository", {}).get("commit", "")
    if graph_commit and provenance.get("source_commit") and provenance["source_commit"] != graph_commit:
        signals.append("proposal source commit differs from graph commit")
    return signals

from __future__ import annotations

from typing import Any

from .models import TOOL_STATES, ToolProposal


def validate_tool_proposal(proposal: ToolProposal, graph: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if proposal.lifecycle_state not in TOOL_STATES:
        errors.append(f"invalid lifecycle state: {proposal.lifecycle_state}")
    if not proposal.permissions:
        errors.append("proposal must declare at least one permission")
    if not proposal.graph_references:
        errors.append("proposal must reference at least one graph node")
    graph_ids = {node.get("id") for node in graph.get("nodes", [])}
    missing_nodes = sorted(set(proposal.graph_references).difference(graph_ids))
    if missing_nodes:
        errors.append(f"proposal references unknown graph nodes: {', '.join(missing_nodes)}")
    if not proposal.data_sources:
        errors.append("proposal must declare a data source")
    if proposal.risk_level != "read_only":
        errors.append("initial foundation only supports read_only proposals")
    if not proposal.provenance.get("graph_id") or not proposal.provenance.get("source_commit"):
        errors.append("proposal must include graph_id and source_commit provenance")
    return errors

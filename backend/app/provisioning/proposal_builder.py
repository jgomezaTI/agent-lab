from __future__ import annotations

import re
from typing import Any

from repository_mapper.provenance import stable_id

from .models import ToolProposal


QUERY_ALIASES = {
    "nota": {"nota", "notas", "grade", "grades"},
    "notas": {"nota", "notas", "grade", "grades"},
    "grade": {"nota", "notas", "grade", "grades"},
    "grades": {"nota", "notas", "grade", "grades"},
    "curso": {"curso", "course"},
    "course": {"curso", "course"},
}


def build_tool_proposal(request_text: str, graph: dict[str, Any], source_commit: str, customer_id: str, product_id: str) -> ToolProposal:
    raw_tokens = {token for token in re.findall(r"[a-zA-Z0-9_]+", request_text.lower()) if len(token) > 2}
    tokens = raw_tokens | {alias for token in raw_tokens for alias in QUERY_ALIASES.get(token, set())}
    candidates = []
    for node in graph.get("nodes", []):
        haystack = f"{node.get('label', '')} {node.get('path', '')}".lower()
        if tokens.intersection(re.findall(r"[a-zA-Z0-9_]+", haystack)):
            candidates.append(node)
    references = sorted({node["id"] for node in candidates})
    assumptions: list[str] = []
    if not references:
        assumptions.append("No graph node matched the request; a product owner must provide evidence.")
    name = "get_course_grades" if {"nota", "notas", "grade", "grades"}.intersection(tokens) else "proposed_read_capability"
    description = f"Read-only capability proposed from request: {request_text.strip()}"
    proposal_id = stable_id("proposal", [request_text, graph.get("graph_id"), customer_id, product_id])
    return ToolProposal(
        proposal_id=proposal_id,
        name=name,
        description=description,
        input_schema={"type": "object", "properties": {"course_id": {"type": "string"}}, "required": ["course_id"]},
        output_schema={"type": "object", "additionalProperties": True},
        permissions=["grades:read"] if name == "get_course_grades" else ["product:read"],
        data_sources=[{"customer_id": customer_id, "product_id": product_id, "interface": "approved_read_only_interface"}],
        risk_level="read_only",
        graph_references=references,
        assumptions=assumptions,
        provenance={"graph_id": graph.get("graph_id", ""), "source_commit": source_commit},
    )

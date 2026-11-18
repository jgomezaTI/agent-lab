from __future__ import annotations

from pathlib import Path
from typing import Any

from .extractors import extract_file_structure
from .models import ApplicationGraph, GraphNode, GraphRelationship, RepositoryScope
from .provenance import ANALYZER_NAME, ANALYZER_VERSION, canonical_json, repository_commit, sha256_text, stable_id
from .scanner import scan_repository


def build_application_graph(root: Path, scope: RepositoryScope, configuration_hash: str) -> ApplicationGraph:
    root = root.resolve()
    commit, dirty = repository_commit(root)
    scanned = scan_repository(root, scope)
    repository_id = stable_id("repository", {"root": root.as_posix(), "commit": commit})
    nodes: list[GraphNode] = [GraphNode(repository_id, "repository", scope.product_id, ".", {"commit": commit, "dirty": dirty})]
    relationships: list[GraphRelationship] = []
    for item in scanned:
        file_nodes, file_relationships = extract_file_structure(item, root)
        nodes.extend(file_nodes)
        relationships.extend(file_relationships)
        file_node = file_nodes[0]
        relationships.append(GraphRelationship(stable_id("rel", [repository_id, file_node.id, "contains"]), repository_id, file_node.id, "contains"))
    nodes = _deduplicate_nodes(nodes)
    relationships = _deduplicate_relationships(relationships)
    stable_payload: dict[str, Any] = {
        "repository": {"commit": commit, "dirty": dirty},
        "scope": scope.to_dict(),
        "nodes": [node.to_dict() for node in nodes],
        "relationships": [relationship.to_dict() for relationship in relationships],
        "analyzer": {"name": ANALYZER_NAME, "version": ANALYZER_VERSION, "configuration_hash": configuration_hash},
    }
    graph_id = f"graph_{sha256_text(canonical_json(stable_payload))[:16]}"
    return ApplicationGraph.now(
        graph_id=graph_id,
        repository={"root": root.as_posix(), "commit": commit, "is_dirty": dirty},
        scope=scope,
        nodes=tuple(nodes),
        relationships=tuple(relationships),
        analyzer={"name": ANALYZER_NAME, "version": ANALYZER_VERSION, "configuration_hash": configuration_hash},
    )


def validate_graph(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ("graph_id", "repository", "scope", "nodes", "relationships", "generated_at", "analyzer"):
        if field not in value:
            errors.append(f"missing graph field: {field}")
    node_ids = {node.get("id") for node in value.get("nodes", []) if isinstance(node, dict)}
    if len(node_ids) != len(value.get("nodes", [])):
        errors.append("node IDs must be unique")
    relationship_ids = [item.get("id") for item in value.get("relationships", []) if isinstance(item, dict)]
    if len(set(relationship_ids)) != len(relationship_ids):
        errors.append("relationship IDs must be unique")
    for relationship in value.get("relationships", []):
        if relationship.get("source") not in node_ids or relationship.get("target") not in node_ids:
            errors.append(f"relationship references unknown node: {relationship.get('id')}")
    return errors


def _deduplicate_nodes(nodes: list[GraphNode]) -> list[GraphNode]:
    return sorted({node.id: node for node in nodes}.values(), key=lambda item: (item.kind, item.id))


def _deduplicate_relationships(relationships: list[GraphRelationship]) -> list[GraphRelationship]:
    return sorted({relationship.id: relationship for relationship in relationships}.values(), key=lambda item: item.id)

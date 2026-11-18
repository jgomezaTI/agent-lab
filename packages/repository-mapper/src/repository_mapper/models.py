from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class RepositoryScope:
    scope_id: str
    product_id: str
    environment: str
    include: tuple[str, ...]
    exclude: tuple[str, ...] = ()
    languages: tuple[str, ...] = ()
    ignore_hidden: bool = True
    follow_symlinks: bool = False
    max_file_size_bytes: int = 1_000_000
    detect_tests: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "scope_id": self.scope_id,
            "product_id": self.product_id,
            "environment": self.environment,
            "include": list(self.include),
            "exclude": list(self.exclude),
            "languages": list(self.languages),
            "ignore_hidden": self.ignore_hidden,
            "follow_symlinks": self.follow_symlinks,
            "analysis": {
                "max_file_size_bytes": self.max_file_size_bytes,
                "detect_tests": self.detect_tests,
            },
        }


@dataclass(frozen=True)
class GraphNode:
    id: str
    kind: str
    label: str
    path: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "kind": self.kind, "label": self.label, "path": self.path, "metadata": self.metadata}


@dataclass(frozen=True)
class GraphRelationship:
    id: str
    source: str
    target: str
    kind: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "source": self.source, "target": self.target, "kind": self.kind, "metadata": self.metadata}


@dataclass(frozen=True)
class ApplicationGraph:
    graph_id: str
    repository: dict[str, Any]
    scope: RepositoryScope
    nodes: tuple[GraphNode, ...]
    relationships: tuple[GraphRelationship, ...]
    generated_at: str
    analyzer: dict[str, str]

    @classmethod
    def now(cls, **kwargs: Any) -> "ApplicationGraph":
        return cls(generated_at=datetime.now(timezone.utc).isoformat(), **kwargs)

    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "repository": self.repository,
            "scope": self.scope.to_dict(),
            "nodes": [node.to_dict() for node in self.nodes],
            "relationships": [relationship.to_dict() for relationship in self.relationships],
            "generated_at": self.generated_at,
            "analyzer": self.analyzer,
        }

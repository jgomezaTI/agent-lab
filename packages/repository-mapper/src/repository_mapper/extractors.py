from __future__ import annotations

import re
from pathlib import Path

from .models import GraphNode, GraphRelationship
from .provenance import stable_id
from .scanner import ScannedFile


IMPORT_PATTERNS = {
    "python": re.compile(r"^(?:from\s+([\w.]+)|import\s+([\w.]+))", re.MULTILINE),
    "javascript": re.compile(r"(?:from|require\()\s*[\"']([^\"']+)", re.MULTILINE),
    "typescript": re.compile(r"(?:from|require\()\s*[\"']([^\"']+)", re.MULTILINE),
    "rust": re.compile(r"^\s*(?:use|mod)\s+([\w:]+)", re.MULTILINE),
}
ENDPOINT_PATTERN = re.compile(r"(?:@(?:app|router|api)\.(?:get|post|put|delete)|(?:app|router)\.(?:get|post|put|delete)|route\s*\()", re.IGNORECASE)


def extract_file_structure(scanned: ScannedFile, root: Path) -> tuple[list[GraphNode], list[GraphRelationship]]:
    relative = scanned.path
    file_id = stable_id("file", relative)
    nodes = [
        GraphNode(
            id=file_id,
            kind="file",
            label=Path(relative).name,
            path=relative,
            metadata={"language": scanned.language, "size_bytes": scanned.size_bytes, "sha256": scanned.sha256},
        )
    ]
    relationships: list[GraphRelationship] = []
    if scanned.is_test:
        test_id = stable_id("test", relative)
        nodes.append(GraphNode(test_id, "test", Path(relative).name, relative, {"language": scanned.language}))
        relationships.append(GraphRelationship(stable_id("rel", [file_id, test_id, "tested_by"]), file_id, test_id, "tested_by"))
    try:
        text = scanned.absolute_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return nodes, relationships
    if ENDPOINT_PATTERN.search(text):
        endpoint_id = stable_id("endpoint", relative)
        nodes.append(GraphNode(endpoint_id, "endpoint", f"endpoint:{relative}", relative, {"evidence": "route declaration"}))
        relationships.append(GraphRelationship(stable_id("rel", [file_id, endpoint_id, "exposes"]), file_id, endpoint_id, "exposes"))
    for dependency in _imports(text, scanned.language):
        dependency_id = stable_id("dependency", dependency)
        nodes.append(GraphNode(dependency_id, "dependency", dependency, relative, {"import": dependency}))
        relationships.append(GraphRelationship(stable_id("rel", [file_id, dependency_id, "depends_on"]), file_id, dependency_id, "depends_on"))
    return nodes, relationships


def _imports(text: str, language: str) -> tuple[str, ...]:
    pattern = IMPORT_PATTERNS.get(language)
    if pattern is None:
        return ()
    results: set[str] = set()
    for match in pattern.finditer(text):
        results.update(value for value in match.groups() if value)
    return tuple(sorted(results))

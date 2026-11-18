from __future__ import annotations

import argparse
import json
from pathlib import Path

from .graph import build_application_graph, validate_graph
from .scope import load_scope


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="repository-mapper", description="Map a scoped repository without executing its code.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan = subparsers.add_parser("scan", help="Generate an application graph")
    scan.add_argument("--scope", required=True, type=Path)
    scan.add_argument("--repository", type=Path)
    scan.add_argument("--output", required=True, type=Path)
    validate = subparsers.add_parser("validate", help="Validate a graph artifact")
    validate.add_argument("graph", type=Path)
    explain = subparsers.add_parser("explain", help="Print a graph summary")
    explain.add_argument("graph", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "scan":
        scope, root, configuration_hash = load_scope(args.scope, args.repository)
        graph = build_application_graph(root, scope, configuration_hash)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(graph.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"graph_id": graph.graph_id, "nodes": len(graph.nodes), "relationships": len(graph.relationships), "output": str(args.output)}))
        return 0
    value = json.loads(args.graph.read_text(encoding="utf-8"))
    errors = validate_graph(value)
    if args.command == "validate":
        if errors:
            for error in errors:
                print(error)
            return 1
        print("valid")
        return 0
    print(json.dumps({"graph_id": value.get("graph_id"), "nodes": len(value.get("nodes", [])), "relationships": len(value.get("relationships", [])), "errors": errors}, indent=2))
    return 1 if errors else 0

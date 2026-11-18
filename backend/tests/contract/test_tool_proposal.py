import unittest

from backend.app.provisioning.proposal_builder import build_tool_proposal
from backend.app.provisioning.validation import validate_tool_proposal


class ToolProposalContractTests(unittest.TestCase):
    def test_course_grades_proposal_is_read_only_and_graph_backed(self):
        graph = {
            "graph_id": "graph_fixture",
            "nodes": [
                {"id": "node_grades", "kind": "file", "label": "grades.py", "path": "app/grades.py"},
            ],
        }
        proposal = build_tool_proposal("buscar mis notas de curso", graph, "commit-1", "customer-a", "portal")
        self.assertEqual(proposal.name, "get_course_grades")
        self.assertEqual(validate_tool_proposal(proposal, graph), [])
        self.assertEqual(proposal.risk_level, "read_only")

    def test_proposal_with_unknown_graph_reference_is_rejected(self):
        graph = {"graph_id": "graph_fixture", "nodes": []}
        proposal = build_tool_proposal("buscar mis notas", graph, "commit-1", "customer-a", "portal")
        proposal.graph_references = ["node_missing"]
        errors = validate_tool_proposal(proposal, graph)
        self.assertTrue(any("unknown graph nodes" in error for error in errors))

import unittest

from backend.app.provisioning.proposal_builder import build_tool_proposal


class ProposalBuilderTests(unittest.TestCase):
    def test_unmatched_request_preserves_unresolved_assumption(self):
        proposal = build_tool_proposal(
            "consultar una capacidad que no existe",
            {"graph_id": "graph_fixture", "nodes": []},
            "commit-1",
            "customer-a",
            "portal",
        )
        self.assertTrue(proposal.assumptions)
        self.assertEqual(proposal.name, "proposed_read_capability")

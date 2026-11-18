import unittest

from backend.app.provisioning.artifacts import approve_artifact, build_artifact
from backend.app.provisioning.models import ValidationCheck
from backend.app.provisioning.publisher import MockPublisher, PublicationDenied
from backend.app.provisioning.proposal_builder import build_tool_proposal


class PublicationContractTests(unittest.TestCase):
    def _artifact(self):
        graph = {"graph_id": "graph_fixture", "nodes": [{"id": "node_grades", "path": "grades.py", "label": "grades.py"}]}
        proposal = build_tool_proposal("notas", graph, "commit-1", "customer-a", "portal")
        return build_artifact(proposal, "commit-1", "graph_fixture", [ValidationCheck("contract", "passed", "ok")])

    def test_unapproved_artifact_cannot_be_published(self):
        with self.assertRaises(PublicationDenied):
            MockPublisher().publish(self._artifact(), "customer-a", "runtime-a")

    def test_approved_artifact_creates_deployment_record(self):
        artifact = self._artifact()
        approve_artifact(artifact, "approver")
        deployment = MockPublisher().publish(artifact, "customer-a", "runtime-a")
        self.assertEqual(deployment["status"], "active")
        self.assertEqual(deployment["transport"], "mcp")
        self.assertEqual(artifact.lifecycle_state, "published")

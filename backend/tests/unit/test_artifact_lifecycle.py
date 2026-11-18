import unittest

from backend.app.provisioning.artifacts import approve_artifact, build_artifact
from backend.app.provisioning.models import ValidationCheck
from backend.app.provisioning.proposal_builder import build_tool_proposal


class ArtifactLifecycleTests(unittest.TestCase):
    def setUp(self):
        graph = {"graph_id": "graph_fixture", "nodes": [{"id": "node_grades", "path": "grades.py", "label": "grades.py"}]}
        self.proposal = build_tool_proposal("notas", graph, "commit-1", "customer-a", "portal")

    def test_failed_validation_cannot_be_approved(self):
        artifact = build_artifact(self.proposal, "commit-1", "graph_fixture", [ValidationCheck("contract", "failed", "bad schema")])
        with self.assertRaises(ValueError):
            approve_artifact(artifact, "approver")

    def test_passing_artifact_keeps_provenance_and_approval(self):
        artifact = build_artifact(self.proposal, "commit-1", "graph_fixture", [ValidationCheck("contract", "passed", "ok")])
        approve_artifact(artifact, "approver")
        self.assertTrue(artifact.is_approved())
        self.assertEqual(artifact.source_commit, "commit-1")
        self.assertTrue(artifact.package_digest)

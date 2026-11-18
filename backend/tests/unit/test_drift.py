import unittest

from backend.app.provisioning.drift import detect_drift


class DriftTests(unittest.TestCase):
    def test_matching_provenance_has_no_drift(self):
        graph = {"graph_id": "graph-1", "repository": {"commit": "commit-1"}}
        proposal = {"provenance": {"graph_id": "graph-1", "source_commit": "commit-1"}}
        self.assertEqual(detect_drift(graph, proposal), [])

    def test_changed_graph_or_commit_is_flagged(self):
        graph = {"graph_id": "graph-2", "repository": {"commit": "commit-2"}}
        proposal = {"provenance": {"graph_id": "graph-1", "source_commit": "commit-1"}}
        self.assertEqual(len(detect_drift(graph, proposal)), 2)

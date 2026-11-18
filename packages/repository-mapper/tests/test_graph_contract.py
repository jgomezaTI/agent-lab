import unittest

from repository_mapper.graph import build_application_graph, validate_graph
from repository_mapper.models import RepositoryScope


class GraphContractTests(unittest.TestCase):
    def test_graph_has_unique_referentially_valid_ids(self):
        scope = RepositoryScope(
            scope_id="contract",
            product_id="portal",
            environment="local",
            include=("packages/repository-mapper/src/**",),
        )
        graph = build_application_graph(__import__("pathlib").Path("."), scope, "configuration-hash")
        value = graph.to_dict()
        self.assertEqual(validate_graph(value), [])
        self.assertTrue(value["repository"]["commit"])
        self.assertTrue(value["analyzer"]["configuration_hash"])

import json
import tempfile
import unittest
from pathlib import Path

from repository_mapper.graph import build_application_graph, validate_graph
from repository_mapper.scope import load_scope


class MapperIntegrationTests(unittest.TestCase):
    def test_graph_is_reproducible_for_same_content_and_scope(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "app").mkdir()
            (root / "app" / "main.py").write_text("from app.grades import get_grades\n@app.get('/grades')\ndef grades(): pass\n", encoding="utf-8")
            (root / "app" / "grades.py").write_text("def get_grades(): return []\n", encoding="utf-8")
            config = root / "scope.toml"
            config.write_text('scope_id = "scope"\nproduct_id = "portal"\nenvironment = "local"\ninclude = ["app/**"]\n', encoding="utf-8")
            scope, loaded_root, config_hash = load_scope(config, root)
            first = build_application_graph(loaded_root, scope, config_hash).to_dict()
            second = build_application_graph(loaded_root, scope, config_hash).to_dict()
            self.assertEqual(first["graph_id"], second["graph_id"])
            self.assertEqual(first["nodes"], second["nodes"])
            self.assertEqual(validate_graph(first), [])
            self.assertGreaterEqual(len(first["nodes"]), 3)

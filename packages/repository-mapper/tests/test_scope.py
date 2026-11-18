import tempfile
import unittest
from pathlib import Path

from repository_mapper.scope import load_scope, matches_scope


class ScopeTests(unittest.TestCase):
    def test_excluded_paths_win_over_included_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = root / "scope.toml"
            config.write_text(
                'scope_id = "scope"\nproduct_id = "portal"\nenvironment = "local"\ninclude = ["app/**"]\nexclude = ["app/generated/**"]\n',
                encoding="utf-8",
            )
            scope, loaded_root, _ = load_scope(config, root)
            self.assertEqual(loaded_root, root.resolve())
            self.assertTrue(matches_scope("app/main.py", scope))
            self.assertFalse(matches_scope("app/generated/client.py", scope))

    def test_invalid_scope_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary) / "scope.toml"
            config.write_text('scope_id = "scope"\nproduct_id = "portal"\nenvironment = "local"\n', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_scope(config, temporary)

    def test_hidden_paths_and_invalid_analysis_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = root / "scope.toml"
            config.write_text(
                'scope_id = "scope"\nproduct_id = "portal"\nenvironment = "local"\ninclude = ["**"]\n\n[analysis]\nmax_file_size_bytes = 0\n',
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_scope(config, root)

            valid = root / "valid.toml"
            valid.write_text('scope_id = "scope"\nproduct_id = "portal"\nenvironment = "local"\ninclude = ["**"]\n', encoding="utf-8")
            scope, _, _ = load_scope(valid, root)
            self.assertFalse(matches_scope(".secrets/token.txt", scope))

    def test_symlink_policy_is_explicit(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = root / "scope.toml"
            config.write_text('scope_id = "scope"\nproduct_id = "portal"\nenvironment = "local"\ninclude = ["app/**"]\nfollow_symlinks = false\n', encoding="utf-8")
            scope, _, _ = load_scope(config, root)
            self.assertFalse(scope.follow_symlinks)

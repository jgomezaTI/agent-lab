from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path

from .models import RepositoryScope
from .scope import is_excluded, matches_scope


LANGUAGE_BY_SUFFIX = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".rs": "rust",
    ".java": "java",
    ".php": "php",
    ".sql": "sql",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".toml": "toml",
    ".md": "markdown",
}


@dataclass(frozen=True)
class ScannedFile:
    path: str
    absolute_path: Path
    language: str
    size_bytes: int
    sha256: str
    is_test: bool


def scan_repository(root: Path, scope: RepositoryScope) -> tuple[ScannedFile, ...]:
    results: list[ScannedFile] = []
    for current, directories, files in os.walk(root, followlinks=scope.follow_symlinks):
        current_path = Path(current)
        if scope.ignore_hidden:
            directories[:] = [name for name in directories if not name.startswith(".")]
        directories[:] = [name for name in directories if not _excluded_parent(current_path / name, root, scope)]
        for filename in sorted(files):
            if scope.ignore_hidden and filename.startswith("."):
                continue
            absolute = current_path / filename
            relative = absolute.relative_to(root).as_posix()
            if not matches_scope(relative, scope) or absolute.is_symlink():
                continue
            try:
                size = absolute.stat().st_size
            except OSError:
                continue
            if size > scope.max_file_size_bytes:
                continue
            language = LANGUAGE_BY_SUFFIX.get(absolute.suffix.lower(), "unknown")
            if scope.languages and language not in scope.languages and language != "unknown":
                continue
            digest = hashlib.sha256()
            try:
                with absolute.open("rb") as handle:
                    for chunk in iter(lambda: handle.read(64 * 1024), b""):
                        digest.update(chunk)
            except OSError:
                continue
            results.append(ScannedFile(relative, absolute, language, size, digest.hexdigest(), _is_test(relative)))
    return tuple(sorted(results, key=lambda item: item.path))


def _excluded_parent(path: Path, root: Path, scope: RepositoryScope) -> bool:
    relative = path.relative_to(root).as_posix()
    return is_excluded(relative, scope) or (scope.ignore_hidden and any(part.startswith(".") for part in path.parts if part not in root.parts))


def _is_test(relative_path: str) -> bool:
    parts = Path(relative_path).parts
    name = parts[-1].lower()
    return any(part.lower() in {"test", "tests", "spec", "specs"} for part in parts) or name.startswith("test_") or ".test." in name

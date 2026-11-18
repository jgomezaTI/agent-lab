from __future__ import annotations

import fnmatch
import tomllib
from pathlib import Path
from typing import Any

from .models import RepositoryScope
from .provenance import canonical_json, sha256_text


VALID_ENVIRONMENTS = {"local", "sandbox", "staging", "production"}


def _as_strings(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{field_name} must be a list of non-empty strings")
    return tuple(value)


def load_scope(config_path: str | Path, repository_root: str | Path | None = None) -> tuple[RepositoryScope, Path, str]:
    config_path = Path(config_path).resolve()
    with config_path.open("rb") as handle:
        raw = tomllib.load(handle)
    root = Path(repository_root or raw.get("repository_root") or config_path.parent).resolve()
    scope_id = raw.get("scope_id")
    product_id = raw.get("product_id")
    environment = raw.get("environment")
    include = _as_strings(raw.get("include"), "include")
    if not isinstance(scope_id, str) or not scope_id:
        raise ValueError("scope_id must be a non-empty string")
    if not isinstance(product_id, str) or not product_id:
        raise ValueError("product_id must be a non-empty string")
    if environment not in VALID_ENVIRONMENTS:
        raise ValueError(f"environment must be one of {sorted(VALID_ENVIRONMENTS)}")
    if not include:
        raise ValueError("include must contain at least one pattern")
    if not root.is_dir():
        raise ValueError(f"repository root does not exist or is not a directory: {root}")
    analysis = raw.get("analysis") or {}
    if not isinstance(analysis, dict):
        raise ValueError("analysis must be a table")
    max_file_size = analysis.get("max_file_size_bytes", 1_000_000)
    if not isinstance(max_file_size, int) or max_file_size < 1:
        raise ValueError("analysis.max_file_size_bytes must be a positive integer")
    scope = RepositoryScope(
        scope_id=scope_id,
        product_id=product_id,
        environment=environment,
        include=include,
        exclude=_as_strings(raw.get("exclude"), "exclude"),
        languages=_as_strings(raw.get("languages"), "languages"),
        ignore_hidden=bool(raw.get("ignore_hidden", True)),
        follow_symlinks=bool(raw.get("follow_symlinks", False)),
        max_file_size_bytes=max_file_size,
        detect_tests=bool(analysis.get("detect_tests", True)),
    )
    return scope, root, sha256_text(canonical_json(scope.to_dict()))


def _pattern_matches(relative_path: str, pattern: str) -> bool:
    normalized = relative_path.strip("/")
    pattern = pattern.strip("/")
    if pattern.endswith("/**"):
        prefix = pattern[:-3].rstrip("/")
        return normalized == prefix or normalized.startswith(prefix + "/")
    return fnmatch.fnmatch(normalized, pattern)


def matches_scope(relative_path: str, scope: RepositoryScope) -> bool:
    relative_path = relative_path.replace("\\", "/").strip("/")
    if scope.ignore_hidden and any(part.startswith(".") for part in Path(relative_path).parts):
        return False
    if is_excluded(relative_path, scope):
        return False
    included = any(_pattern_matches(relative_path, pattern) for pattern in scope.include)
    if included:
        return True
    parts = relative_path.split("/")
    return any(any(_pattern_matches("/".join(parts[:index]), pattern) for pattern in scope.include) for index in range(1, len(parts)))


def is_excluded(relative_path: str, scope: RepositoryScope) -> bool:
    relative_path = relative_path.replace("\\", "/").strip("/")
    return any(_pattern_matches(relative_path, pattern) for pattern in scope.exclude)

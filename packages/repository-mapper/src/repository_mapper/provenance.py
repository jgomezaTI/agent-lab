from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ANALYZER_NAME = "agentlab-repository-mapper"
ANALYZER_VERSION = "0.1.0"


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def stable_id(prefix: str, value: Any) -> str:
    return f"{prefix}_{sha256_text(canonical_json(value))[:16]}"


def repository_commit(root: Path) -> tuple[str, bool]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], cwd=root, check=True, capture_output=True, text=True
        ).stdout.strip() != ""
        return commit or "unknown", dirty
    except (OSError, subprocess.CalledProcessError):
        return "unknown", False

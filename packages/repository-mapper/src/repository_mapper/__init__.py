"""Deterministic, repository-only application mapping primitives."""

__version__ = "0.1.0"

from .graph import build_application_graph
from .scope import load_scope

__all__ = ["__version__", "build_application_graph", "load_scope"]

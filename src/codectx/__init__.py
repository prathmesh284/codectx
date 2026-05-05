"""CodeCtx package metadata and lazy exports."""

from importlib.metadata import PackageNotFoundError, version
from importlib import import_module

try:
    __version__ = version("pycodectx")
except PackageNotFoundError:
    __version__ = "1.0.2"

__all__ = [
    "AnalysisContext",
    "FileAnalysis",
    "AnalysisService",
    "FileSystemService",
    "CLIHandler",
]


def __getattr__(name):
    """Lazily expose the public API without import-time side effects."""
    if name in {"AnalysisContext", "FileAnalysis"}:
        return getattr(import_module("codectx.models"), name)
    if name in {"AnalysisService", "FileSystemService"}:
        return getattr(import_module("codectx.services"), name)
    if name == "CLIHandler":
        return getattr(import_module("codectx.cli"), name)
    raise AttributeError(f"module 'codectx' has no attribute {name!r}")

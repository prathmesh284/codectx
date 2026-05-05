# models/__init__.py
"""Data models and schemas for CodeCtx."""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AnalysisContext:
    """Complete analysis context for a project."""
    project: str
    file_tree: List[str]
    analysis_time: str
    functions: Dict[str, List[str]] = field(default_factory=dict)
    summaries: Dict[str, str] = field(default_factory=dict)
    api_endpoints: Dict[str, List[Dict]] = field(default_factory=dict)
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    env: List[str] = field(default_factory=list)
    data_flow: Dict[str, List[str]] = field(default_factory=dict)
    secrets: Dict[str, List[str]] = field(default_factory=dict)
    plugins: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    function_details: Dict[str, List[Dict]] = field(default_factory=dict)
    auth_info: Dict[str, List[str]] = field(default_factory=dict)
    error_analysis: Dict[str, Dict] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "project": self.project,
            "file_tree": self.file_tree,
            "functions": self.functions,
            "summaries": self.summaries,
            "api_endpoints": self.api_endpoints,
            "dependencies": self.dependencies,
            "env": self.env,
            "data_flow": self.data_flow,
            "secrets": self.secrets,
            "plugins": self.plugins,
            "function_details": self.function_details,
            "auth_info": self.auth_info,
            "error_analysis": self.error_analysis,
            "analysis_time": self.analysis_time,
        }


@dataclass
class FileAnalysis:
    """Analysis results for a single file."""
    file: str
    functions: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    apis: List[Dict] = field(default_factory=list)
    flow: List[str] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)
    env: List[str] = field(default_factory=list)
    summary: str = ""
    plugins: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    function_details: List[Dict] = field(default_factory=list)
    auth_info: List[str] = field(default_factory=list)
    error_analysis: Dict[str, Any] = field(default_factory=dict)

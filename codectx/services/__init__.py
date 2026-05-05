# services/__init__.py
"""High-level services for project analysis."""

import os
from datetime import datetime
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor

from ..core.utils import detect_language, clean_dependencies
from ..core.scanner import build_file_tree
from ..extractors.functions import extract_functions, extract_function_details
from ..extractors.apis import extract_apis
from ..extractors.dependencies import extract_dependencies
from ..extractors.env import extract_env
from ..extractors.secrets import detect_secrets
from ..processors.summary import generate_summary
from ..processors.dataflow import detect_data_flow
from ..processors.error_analysis import analyze_errors
from ..processors.auth import detect_auth
from ..plugins.manager import run_plugins
from ..models import AnalysisContext, FileAnalysis


class AnalysisService:
    """Main service for orchestrating project analysis."""

    def __init__(self, max_workers: int = 8):
        self.max_workers = max_workers

    def analyze_single_file(self, file: str, use_reload: bool = False) -> FileAnalysis:
        """Analyze a single file."""
        try:
            with open(file, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception:
            return None

        lang = detect_language(file)

        # Core analysis
        funcs = extract_functions(code, lang)
        deps = clean_dependencies(extract_dependencies(code))
        apis = extract_apis(code)
        flow = detect_data_flow(code, file)
        secrets = detect_secrets(code)
        envs = extract_env(code)
        func_detail = extract_function_details(code)
        auth = detect_auth(code)
        error_info = analyze_errors(code, file, lang)
        plugin_results = run_plugins(file, code, lang, use_reload)

        return FileAnalysis(
            file=file,
            functions=funcs,
            dependencies=deps,
            apis=apis,
            flow=flow,
            secrets=secrets,
            env=envs,
            summary=generate_summary(file, lang, funcs, deps, apis),
            plugins=plugin_results,
            function_details=func_detail,
            auth_info=auth,
            error_analysis=error_info,
        )

    def analyze_project(
        self, files, root: str, use_reload: bool = False
    ) -> AnalysisContext:
        """Analyze entire project."""
        ctx = AnalysisContext(
            project=os.path.basename(os.path.abspath(root)),
            file_tree=files,
            analysis_time=datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(),
        )

        # Parallel file analysis
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(
                filter(
                    None,
                    executor.map(
                        lambda f: self.analyze_single_file(f, use_reload), files
                    ),
                )
            )

        # Aggregate results
        for r in results:
            file = r.file
            ctx.functions[file] = r.functions
            ctx.dependencies[file] = r.dependencies
            ctx.api_endpoints[file] = r.apis
            ctx.data_flow[file] = r.flow
            ctx.secrets[file] = r.secrets
            ctx.summaries[file] = r.summary
            ctx.plugins[file] = r.plugins
            ctx.function_details[file] = r.function_details
            ctx.auth_info[file] = r.auth_info
            ctx.error_analysis[file] = r.error_analysis

            for e in r.env:
                ctx.env.append(e)

        ctx.env = list(set(ctx.env))  # Remove duplicates
        return ctx


class FileSystemService:
    """Service for file system operations."""

    @staticmethod
    def scan_project(path: str) -> list:
        """Scan project and return file list."""
        return build_file_tree(path)

    @staticmethod
    def get_file_content(filepath: str) -> str:
        """Read file content."""
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

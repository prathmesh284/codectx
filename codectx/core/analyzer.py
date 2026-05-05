# core/analyzer.py
import os
from concurrent.futures import ThreadPoolExecutor
from core.utils import detect_language, clean_dependencies
from extractors.functions import extract_functions, extract_function_details
from extractors.apis import extract_apis
from extractors.dependencies import extract_dependencies
from extractors.env import extract_env
from extractors.secrets import detect_secrets
from processors.summary import generate_summary
from processors.dataflow import detect_data_flow
from processors.error_analysis import analyze_errors
from processors.auth import detect_auth
from plugins.manager import run_plugins

# -----------------------------
# Analyze a single file
# -----------------------------
def analyze_file(file, use_reload=False):
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

    # Plugins
    plugin_results = run_plugins(file, code, lang, use_reload)

    return {
        "file": file,
        "functions": funcs,
        "dependencies": deps,
        "apis": apis,
        "flow": flow,
        "secrets": secrets,
        "env": envs,
        "summary": generate_summary(file, lang, funcs, deps, apis),
        "plugins": plugin_results,
        "function_details": func_detail,
        "auth_info": auth,
        "error_analysis": error_info
    }

# -----------------------------
# Analyze entire project (parallel)
# -----------------------------
def analyze_project(files, root, use_reload=False, max_workers=8):
    ctx = {
        "project": os.path.basename(os.path.abspath(root)),
        "file_tree": files,
        "functions": {},
        "summaries": {},
        "api_endpoints": {},
        "dependencies": {},
        "env": set(),
        "data_flow": {},
        "secrets": {},
        "plugins": {},
        "function_details": {},
        "auth_info": {},
        "error_analysis": {}
    }

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(filter(None, executor.map(
            lambda f: analyze_file(f, use_reload), files
        )))

    for r in results:
        file = r["file"]
        ctx["functions"][file] = r["functions"]
        ctx["dependencies"][file] = r["dependencies"]
        ctx["api_endpoints"][file] = r["apis"]
        ctx["data_flow"][file] = r["flow"]
        ctx["secrets"][file] = r["secrets"]
        ctx["summaries"][file] = r["summary"]
        ctx["plugins"][file] = r["plugins"]
        ctx["function_details"][file] = r["function_details"]
        ctx["auth_info"][file] = r["auth_info"]
        ctx["error_analysis"][file] = r["error_analysis"]

        for e in r["env"]:
            ctx["env"].add(e)

    ctx["env"] = list(ctx["env"])
    return ctx
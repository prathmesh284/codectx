def detect_language(file):
    ext = file.split(".")[-1].lower()

    return {
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "jsx": "javascript",
        "tsx": "typescript",
        "java": "java",
        "go": "go",
        "rs": "rust",
        "cpp": "cpp",
        "c": "c",
        "yaml": "yaml",
        "yml": "yaml",
        "json": "json",
        "sh": "shell",
        "tf": "terraform",
        "sql": "sql",
        "md": "text",
        "css": "style"
    }.get(ext, "unknown")


def clean_dependencies(deps):
    return [d for d in set(deps) if len(d) > 2 and not d.startswith(".")]
def generate_summary(file, lang, funcs, deps, apis):
    if lang in ["json", "yaml", "style", "text"]:
        return "config/static file"

    parts = []

    if apis:
        parts.append("API handler")

    if any("auth" in f.lower() for f in funcs):
        parts.append("authentication")

    if any("sql" in d.lower() or "db" in d.lower() for d in deps):
        parts.append("database usage")

    if not parts:
        return "utility/module"

    return ", ".join(parts)
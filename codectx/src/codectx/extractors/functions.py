import re
import ast


def extract_functions(code, lang):
    if lang == "python":
        try:
            tree = ast.parse(code)
            return [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        except SyntaxError:
            return []

    patterns = {
        "javascript": r'function\s+(\w+)|const\s+(\w+)\s*=\s*\(',
        "typescript": r'function\s+(\w+)|const\s+(\w+)\s*=\s*\(',
        "java": r'(?:public|private|protected)\s+\w+\s+(\w+)\(',
        "go": r'func\s+(\w+)',
        "rust": r'fn\s+(\w+)',
        "cpp": r'\w+\s+(\w+)\s*\(.*\)\s*{',
        "c": r'\w+\s+(\w+)\s*\(.*\)\s*{',
    }

    funcs = set()
    pattern = patterns.get(lang)

    if pattern:
        matches = re.findall(pattern, code)
        for m in matches:
            if isinstance(m, tuple):
                funcs.update([x for x in m if x])
            else:
                funcs.add(m)

    blacklist = {"if", "for", "while", "switch"}
    return [f for f in funcs if f not in blacklist]


def extract_function_details(code):
    results = []

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                inputs = [arg.arg for arg in node.args.args]

                results.append({
                    "name": node.name,
                    "inputs": inputs,
                    "output": "unknown",
                    "description": "function logic",
                })

    except SyntaxError:
        pass

    return results

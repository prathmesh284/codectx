import re

def extract_dependencies(code):
    patterns = [
        r'import\s+.*?from\s+[\'"](.*?)[\'"]',
        r'import\s+(\w+)',
        r'from\s+(\w+)',
        r'#include\s+[<"](.*?)[>"]'
    ]

    deps = set()

    for p in patterns:
        matches = re.findall(p, code)
        for m in matches:
            if isinstance(m, tuple):
                deps.update(m)
            else:
                deps.add(m)

    return list(deps)
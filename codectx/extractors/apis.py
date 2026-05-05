import re

def extract_apis(code):
    patterns = [
        r'@(app|router)\.(get|post|put|delete|patch)\(["\'](.*?)["\']\)',
        r'app\.(get|post|put|delete)\(["\'](.*?)["\']',
        r'@(GetMapping|PostMapping|PutMapping|DeleteMapping)\(["\'](.*?)["\']\)'
    ]

    apis = []

    for p in patterns:
        matches = re.findall(p, code)
        for m in matches:
            if len(m) == 3:
                apis.append({"method": m[1].upper(), "path": m[2]})
            elif len(m) == 2:
                apis.append({"method": m[0].upper(), "path": m[1]})

    return dedupe(apis)


def dedupe(items):
    seen = set()
    result = []

    for item in items:
        key = tuple(item.items())
        if key not in seen:
            seen.add(key)
            result.append(item)

    return result
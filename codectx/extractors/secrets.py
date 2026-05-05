import re

def detect_secrets(code):
    patterns = [
        r'API_KEY\s*=\s*["\'].*?["\']',
        r'SECRET\s*=\s*["\'].*?["\']',
        r'password\s*=\s*["\'].*?["\']'
    ]

    return [m for p in patterns for m in re.findall(p, code)]
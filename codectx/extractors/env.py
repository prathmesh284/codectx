import re

def extract_env(code):
    return re.findall(r'os\.getenv\(["\'](.*?)["\']', code)
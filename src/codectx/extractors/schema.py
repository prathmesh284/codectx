import re

def extract_schema(code):
    tables = {}

    matches = re.findall(r'class\s+(\w+)\(.*?Base.*?\):(.*?)(?=class|\Z)', code, re.S)

    for name, body in matches:
        fields = re.findall(r'(\w+)\s*=\s*Column', body)
        tables[name] = fields

    return tables
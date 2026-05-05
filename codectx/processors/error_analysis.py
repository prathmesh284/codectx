import re

def analyze_errors(code, file, lang):
    result = {
        "has_error_handling": False,
        "patterns": [],
        "risky_areas": [],
        "missing_handling": []
    }

    # -----------------------------
    # 🐍 Python Analysis
    # -----------------------------
    if lang == "python":
        try_blocks = re.findall(r'try:(.*?)except\s+(.*?):', code, re.S)

        for block, exception in try_blocks:
            result["has_error_handling"] = True

            result["patterns"].append({
                "type": "try_except",
                "exceptions": [exception.strip()],
                "has_finally": "finally" in code
            })

    # -----------------------------
    # 🌐 JS / TS Analysis
    # -----------------------------
    elif lang in ["javascript", "typescript"]:
        try_blocks = re.findall(r'try\s*{(.*?)}\s*catch\s*\((.*?)\)', code, re.S)

        for block, exception in try_blocks:
            result["has_error_handling"] = True

            result["patterns"].append({
                "type": "try_catch",
                "exceptions": [exception.strip()],
                "has_finally": "finally" in code
            })

    # -----------------------------
    # ⚠️ Risky Area Detection
    # -----------------------------
    if "fetch(" in code or "axios" in code:
        result["risky_areas"].append("external API call")

    if "sqlalchemy" in code.lower() or "session" in code:
        result["risky_areas"].append("database operation")

    if "open(" in code:
        result["risky_areas"].append("file handling")

    # -----------------------------
    # 🚨 Missing Handling Detection
    # -----------------------------
    if ("fetch(" in code or "axios" in code) and "catch" not in code:
        result["missing_handling"].append("no API error handling")

    if "timeout" not in code and ("fetch(" in code or "requests" in code):
        result["missing_handling"].append("no timeout handling")

    if "retry" not in code and ("fetch(" in code or "requests" in code):
        result["missing_handling"].append("no retry logic")

    return result
def detect_data_flow(code, file):
    if not file.endswith((".py", ".js", ".ts")):
        return []

    flow = []

    if "fetch(" in code or "axios" in code:
        flow.append("frontend → api")

    if "sqlalchemy" in code.lower() or "commit(" in code or "session" in code:
        flow.append("database interaction")

    if "generate_response" in code:
        flow.append("API → AI Engine")
        
    return flow
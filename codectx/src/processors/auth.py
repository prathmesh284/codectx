def detect_auth(code):
    flow = []

    if "next-auth" in code.lower():
        flow.append("OAuth → NextAuth session")

    if "jwt" in code.lower():
        flow.append("JWT authentication")

    return flow
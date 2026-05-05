# plugins/todo_detector.py
from codectx.src.plugins.base import BasePlugin

class Plugin(BasePlugin):
    name = "todo-detector"
    capabilities = ["detect_todos", "list_for_review"]

    def supports(self, file, lang):
        # For demo, support all files
        return True

    def analyze(self, file, code):
        todos = [line.strip() for line in code.split("\n") if "TODO" in line]
        return {"todos": todos}

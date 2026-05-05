# plugins/base.py
class BasePlugin:
    """
    Base class for all plugins.
    """

    name = "base"
    capabilities = []  # ✅ Make this an attribute to allow JSON serialization

    def supports(self, file, lang):
        """
        Return True if this plugin can analyze the given file/language.
        """
        return False

    def analyze(self, file, code):
        """
        Perform analysis and return results as a JSON-serializable dict.
        """
        return {}
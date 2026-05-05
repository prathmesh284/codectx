# plugins/loader.py
import os
import importlib.util

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

def load_plugins():
    """
    Load all plugins dynamically from the plugins folder.
    Returns a list of plugin instances.
    """
    plugins = []

    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith(".py") and filename not in ["base.py", "loader.py", "manager.py", "__init__.py"]:
            path = os.path.join(PLUGIN_DIR, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "Plugin"):
                plugins.append(module.Plugin())

    return plugins
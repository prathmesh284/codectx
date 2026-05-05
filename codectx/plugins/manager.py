import os
import sys
import shutil
import importlib.util

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_PACKAGE = "codectx.plugins"
LOADED_PLUGINS = []

def load_plugins():
    """
    Load all plugins dynamically from the plugins folder.
    Updates the global LOADED_PLUGINS cache.
    Returns a list of plugin instances.
    """
    global LOADED_PLUGINS
    LOADED_PLUGINS.clear()

    for f in os.listdir(PLUGIN_DIR):
        if f.endswith(".py") and f not in ["base.py", "manager.py", "__init__.py"]:
            module_name = f[:-3]
            path = os.path.join(PLUGIN_DIR, f)
            qualified_name = f"{PLUGIN_PACKAGE}.{module_name}"
            spec = importlib.util.spec_from_file_location(qualified_name, path)
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            sys.modules[qualified_name] = module
            spec.loader.exec_module(module)
            if hasattr(module, "Plugin"):
                LOADED_PLUGINS.append(module.Plugin())
    return LOADED_PLUGINS


def reload_plugins():
    """
    Force reload of all plugin files.
    Clears sys.modules cache and re-imports everything.
    """
    # Remove plugin modules from sys.modules
    for f in os.listdir(PLUGIN_DIR):
        if f.endswith(".py") and f not in ["base.py", "manager.py", "__init__.py"]:
            module_name = f[:-3]
            sys.modules.pop(f"{PLUGIN_PACKAGE}.{module_name}", None)
    
    return load_plugins()


def run_plugins(file, code, lang, use_reload=False):
    """
    Execute all plugins for a file and return JSON-serializable results.
    
    Args:
        file: File path being analyzed
        code: File contents
        lang: Detected language
        use_reload: If True, force reload plugins before running
    
    Returns:
        Dictionary with plugin results (JSON-serializable)
    """
    # Reload plugins if explicitly requested
    if use_reload:
        plugins = reload_plugins()
    else:
        # Use cached plugins, but load them if not already loaded
        if not LOADED_PLUGINS:
            load_plugins()
        plugins = LOADED_PLUGINS

    results = {}
    
    for plugin in plugins:
        try:
            if plugin.supports(file, lang):
                data = plugin.analyze(file, code)
                if data:
                    results[plugin.name] = {
                        "capabilities": getattr(plugin, "capabilities", []),
                        "result": data
                    }
        except Exception as e:
            results[plugin.name] = {
                "capabilities": getattr(plugin, "capabilities", []),
                "error": str(e)
            }

    return results


def add_plugin_file(filepath, target_dir=None):
    """
    Copy a plugin file into the plugin directory.
    
    Args:
        filepath: Path to the plugin file to add
        target_dir: Target directory (default: PLUGIN_DIR)
    
    Returns:
        Destination path of the added plugin
    
    Raises:
        FileNotFoundError: If source file doesn't exist
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Plugin file '{filepath}' not found")
    
    # Use default plugin directory if not specified
    if target_dir is None:
        target_dir = PLUGIN_DIR
    else:
        # Resolve relative paths
        target_dir = os.path.abspath(target_dir)
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir, exist_ok=True)
    
    filename = os.path.basename(filepath)
    dest = os.path.join(target_dir, filename)
    
    # Avoid overwriting if same source and dest
    source_abs = os.path.abspath(filepath)
    if os.path.abspath(dest) == source_abs:
        return dest
    
    shutil.copyfile(filepath, dest)
    return dest


def list_plugins(target_dir=None):
    """
    List all available plugins in a directory.
    
    Args:
        target_dir: Directory to list (default: PLUGIN_DIR)
    
    Returns:
        List of plugin filenames
    """
    if target_dir is None:
        plugins = LOADED_PLUGINS if LOADED_PLUGINS else load_plugins()
        return [p.name for p in plugins]
    else:
        target_dir = os.path.abspath(target_dir)
        if not os.path.isdir(target_dir):
            return []
        
        plugin_files = []
        for f in os.listdir(target_dir):
            if f.endswith(".py") and f not in ["base.py", "manager.py", "__init__.py"]:
                plugin_files.append(f[:-3])  # Remove .py extension
        return plugin_files


def remove_plugin(name, target_dir=None):
    """
    Remove a plugin by name.
    
    Args:
        name: Plugin name or filename (with or without .py)
        target_dir: Directory to search (default: PLUGIN_DIR)
    
    Returns:
        True if removed, False if not found
    """
    if target_dir is None:
        target_dir = PLUGIN_DIR
    else:
        target_dir = os.path.abspath(target_dir)
    
    # Normalize name (allow both "plugin" and "plugin.py")
    if not name.endswith(".py"):
        name = name + ".py"
    
    plugin_path = os.path.join(target_dir, name)
    
    if os.path.exists(plugin_path):
        os.remove(plugin_path)
        return True
    
    return False


# Initialize plugins on module load
load_plugins()

"""Legacy configuration - use config_manager.py for new code."""

# Legacy values (for backward compatibility)
PROJECT_ROOT = "./"
OUTPUT_FILE = "project.ctx.json"

IGNORE_DIRS = ["venv", "node_modules", ".git", "__pycache__"]
IGNORE_FILES = [".ctx.json"]

# For new code, use config_manager instead:
# from config_manager import get_config_manager
# cm = get_config_manager()
# project_root = cm.get("project_root", "./")
# output_file = cm.get("output_file", "project.ctx.json")
# ignore_dirs = cm.get("ignore_dirs", [])

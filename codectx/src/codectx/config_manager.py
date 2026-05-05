"""Auto-configuration and initialization for CodeCtx."""

import os
import json
import sys
import tempfile
from pathlib import Path

# Try to load .env file
try:
    from dotenv import load_dotenv
    # Load from .env file if it exists
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, continue without it


class ConfigManager:
    """Manages configuration with auto-initialization on first run."""

    # Config directory locations by OS
    CONFIG_DIRS = {
        "win32": Path.home() / "AppData" / "Local" / "CodeCtx",
        "darwin": Path.home() / ".config" / "codectx",  # macOS
        "linux": Path.home() / ".config" / "codectx",   # Linux
    }

    def __init__(self):
        self._set_config_paths(self._get_config_dir())
        self.ensure_initialized()

    def _set_config_paths(self, config_dir: Path) -> None:
        """Update all paths derived from the config directory."""
        self.config_dir = config_dir
        self.config_file = self.config_dir / "config.json"
        self.plugins_dir = self.config_dir / "plugins"

    def _get_config_dir(self) -> Path:
        """Get platform-specific config directory.
        
        Priority:
        1. CODECTX_CONFIG_DIR environment variable (if set)
        2. Platform-specific default directory
        """
        # Check for environment variable override
        env_config_dir = os.getenv("CODECTX_CONFIG_DIR")
        if env_config_dir:
            return Path(env_config_dir.strip()).expanduser().resolve()
        
        # Use platform-specific defaults
        platform = sys.platform
        config_dir = self.CONFIG_DIRS.get(platform, Path.home() / ".codectx")
        return config_dir.resolve()

    def ensure_initialized(self) -> None:
        """Ensure config directory and files exist (auto-init on first run)."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            self.plugins_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            fallback_dir = Path(tempfile.gettempdir()) / "codectx"
            self._set_config_paths(fallback_dir.resolve())
            self.config_dir.mkdir(parents=True, exist_ok=True)
            self.plugins_dir.mkdir(parents=True, exist_ok=True)
            print(f"Config directory not writable, using fallback: {self.config_dir}")

        # Create default config if it doesn't exist
        if not self.config_file.exists():
            self._create_default_config()

    def _create_default_config(self) -> None:
        """Create default configuration file."""
        default_config = {
            "project_root": "./",
            "output_file": "project.ctx.json",
            "ignore_dirs": [
                "venv",
                "node_modules",
                ".git",
                "__pycache__",
                ".env",
                "dist",
                "build",
                ".pytest_cache",
                ".mypy_cache",
            ],
            "ignore_files": [".ctx.json", ".DS_Store", "*.pyc"],
            "verbose": False,
            "plugins_enabled": True,
            "auto_backup": True,
        }

        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2)

        print(f"Configuration initialized at: {self.config_file}")

    def load_config(self) -> dict:
        """Load configuration from file."""
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def update_config(self, key: str, value) -> None:
        """Update a configuration value."""
        config = self.load_config()
        config[key] = value

        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    def get(self, key: str, default=None):
        """Get configuration value."""
        config = self.load_config()
        return config.get(key, default)

    def get_config_dir(self) -> Path:
        """Get configuration directory path."""
        return self.config_dir

    def get_plugins_dir(self) -> Path:
        """Get plugins directory path."""
        return self.plugins_dir


# Global instance
_config_manager = None


def get_config_manager() -> ConfigManager:
    """Get or create config manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def reset_config_manager() -> None:
    """Reset the cached config manager instance.

    This is primarily useful in tests that change environment variables.
    """
    global _config_manager
    _config_manager = None

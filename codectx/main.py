# main.py
"""CodeCtx main entry point."""

from .config_manager import get_config_manager
from .cli import CLIHandler


def main():
    """Main application entry point."""
    # Initialize configuration (auto-config on first run)
    get_config_manager()

    # Run CLI handler
    handler = CLIHandler()
    handler.run()


if __name__ == "__main__":
    main()

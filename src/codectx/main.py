"""CodeCtx main entry point."""

from __future__ import annotations

import sys
import warnings

from .config_manager import get_config_manager
from .cli import CLIHandler

# Suppress SyntaxWarnings about invalid escape sequences in analyzed code
warnings.filterwarnings("ignore", category=SyntaxWarning, message=r".*invalid escape sequence.*")


def main(argv: list[str] | None = None) -> int:
    """Main application entry point."""
    args = list(sys.argv[1:] if argv is None else argv)

    if args and args[0] == "setup":
        from .setup import main as setup_main

        return setup_main(args[1:])

    get_config_manager()
    handler = CLIHandler()
    handler.run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

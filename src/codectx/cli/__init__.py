# cli/__init__.py
"""Command-line interface for CodeCtx."""

import argparse
from ..services import AnalysisService, FileSystemService
from ..output.writer import write_output
from ..plugins.manager import add_plugin_file, remove_plugin, list_plugins
from ..config_manager import get_config_manager
from ..utils import FormattingUtils


class CLIHandler:
    """Handles command-line arguments and execution."""

    def __init__(self):
        self.config_manager = get_config_manager()
        self.parser = self._create_parser()
        self.analysis_service = AnalysisService()
        self.fs_service = FileSystemService()
        self.fmt = FormattingUtils()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser with subcommands."""
        project_root = self.config_manager.get("project_root", "./")
        
        parser = argparse.ArgumentParser(
            description="CodeCtx - Advanced Code Analysis",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  codectx .                              # Analyze current directory
  codectx /path --verbose                # Analyze with verbose output
  codectx . --reload-plugins             # Reload plugins before analysis
  codectx plugin add /path/to/plugin.py  # Add plugin to default location
  codectx plugin add plugin.py --dir ./my_plugins  # Add plugin to custom directory
  codectx plugin remove my_plugin        # Remove plugin
  codectx plugin list                    # List all plugins
            """
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Commands")
        subparsers.required = False
        
        # Analyze command (default)
        analyze_parser = subparsers.add_parser("analyze", help="Analyze a project")
        analyze_parser.add_argument("path", nargs="?", default=project_root, help="Path to scan")
        analyze_parser.add_argument(
            "--reload-plugins", action="store_true", help="Hot reload plugins for development"
        )
        analyze_parser.add_argument("--verbose", action="store_true", help="Show detailed logs")
        
        # Plugin commands
        plugin_parser = subparsers.add_parser("plugin", help="Manage plugins")
        plugin_subparsers = plugin_parser.add_subparsers(dest="plugin_cmd", help="Plugin operations")
        plugin_subparsers.required = False
        
        # plugin add
        add_parser = plugin_subparsers.add_parser("add", help="Add a plugin")
        add_parser.add_argument("file", help="Path to plugin file")
        add_parser.add_argument(
            "--dir", help="Target directory (default: plugins folder)"
        )
        
        # plugin remove
        remove_parser = plugin_subparsers.add_parser("remove", help="Remove a plugin")
        remove_parser.add_argument("name", help="Plugin name (with or without .py)")
        remove_parser.add_argument("--dir", help="Directory containing plugin (default: plugins folder)")
        
        # plugin list
        list_parser = plugin_subparsers.add_parser("list", help="List available plugins")
        list_parser.add_argument("--dir", help="Directory to list (default: plugins folder)")
        
        return parser

    def handle_plugin_add(self, plugin_file: str, target_dir: str = None) -> None:
        """Handle plugin addition."""
        try:
            dest = add_plugin_file(plugin_file, target_dir)
            print(self.fmt.format_plugin(f"Added successfully: {dest}"))
        except FileNotFoundError as e:
            print(self.fmt.format_error(str(e)))
        except Exception as e:
            print(self.fmt.format_error(f"Failed to add plugin: {e}"))

    def handle_plugin_remove(self, name: str, target_dir: str = None) -> None:
        """Handle plugin removal."""
        try:
            result = remove_plugin(name, target_dir)
            if result:
                print(self.fmt.format_ok(f"Plugin removed: {name}"))
            else:
                print(self.fmt.format_warn(f"Plugin not found: {name}"))
        except Exception as e:
            print(self.fmt.format_error(f"Failed to remove plugin: {e}"))

    def handle_plugin_list(self, target_dir: str = None) -> None:
        """Handle plugin listing."""
        try:
            plugins = list_plugins(target_dir)
            if plugins:
                print(self.fmt.format_ok(f"Available plugins ({len(plugins)}):"))
                for plugin in plugins:
                    print(f"  - {plugin}")
            else:
                print(self.fmt.format_warn("No plugins found"))
        except Exception as e:
            print(self.fmt.format_error(f"Failed to list plugins: {e}"))

    def handle_project_analysis(
        self, path: str, use_reload: bool = False, verbose: bool = False
    ) -> None:
        """Handle project analysis command."""
        output_file = self.config_manager.get("output_file", "project.ctx.json")
        auto_backup = self.config_manager.get("auto_backup", True)
        
        print(self.fmt.format_scan(f"Scanning project at: {path}"))

        files = self.fs_service.scan_project(path)
        print(self.fmt.format_ok(f"Found {len(files)} files"))

        ctx = self.analysis_service.analyze_project(files, path, use_reload=use_reload)

        write_output(ctx, output_file, auto_backup=auto_backup)
        print(self.fmt.format_ok(f"Output written -> {output_file}"))

        if verbose:
            self._print_verbose_summary(ctx)

    def _print_verbose_summary(self, ctx) -> None:
        """Print verbose plugin summary."""
        print(self.fmt.format_info("Plugin summary per file:"))
        for file, plugin_res in ctx.plugins.items():
            print(f"  {file}: {list(plugin_res.keys())}")

    def run(self, args=None):
        """Main entry point."""
        import sys
        
        # Get arguments (use sys.argv[1:] if args not provided)
        if args is None:
            args = sys.argv[1:]
        
        # Legacy mode detection: if first arg is not a known subcommand and doesn't start with hyphen,
        # treat it as a path
        if args and args[0] not in ["plugin", "analyze", "-h", "--help"]:
            # Check if it looks like a path (doesn't start with -)
            if not args[0].startswith("-"):
                # Insert "analyze" command
                args = ["analyze"] + args
        
        parsed_args = self.parser.parse_args(args)

        # Check which command was invoked
        command = getattr(parsed_args, "command", None)
        
        if command == "plugin":
            plugin_cmd = getattr(parsed_args, "plugin_cmd", None)
            if plugin_cmd == "add":
                target_dir = getattr(parsed_args, "dir", None)
                self.handle_plugin_add(parsed_args.file, target_dir)
            elif plugin_cmd == "remove":
                target_dir = getattr(parsed_args, "dir", None)
                self.handle_plugin_remove(parsed_args.name, target_dir)
            elif plugin_cmd == "list":
                target_dir = getattr(parsed_args, "dir", None)
                self.handle_plugin_list(target_dir)
            else:
                print(self.fmt.format_error("Plugin command required: add, remove, or list"))
                self.parser.parse_args(["plugin", "--help"])
        elif command == "analyze":
            # Explicit analyze command
            self.handle_project_analysis(
                parsed_args.path,
                use_reload=parsed_args.reload_plugins,
                verbose=parsed_args.verbose,
            )
        else:
            self.parser.print_help()

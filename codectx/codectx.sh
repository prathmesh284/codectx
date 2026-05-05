#!/bin/bash

# CodeCtx - Advanced Code Analysis Tool
# Modular Architecture v2.0.0

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Show help
show_help() {
    cat << EOF

CodeCtx - Advanced Code Analysis Tool
Version 2.0.0 (Modular Architecture)

USAGE:
  codectx [path] [options]                 Analyze a project
  codectx analyze [path] [options]         Analyze a project (explicit)
  codectx plugin add <file> [--dir <dir>]   Add a plugin
  codectx plugin remove <name> [--dir <dir>] Remove a plugin
  codectx plugin list [--dir <dir>]        List plugins
  codectx help                             Show this help message

OPTIONS:
  --reload-plugins                        Force reload plugins (development)
  --verbose                               Show detailed output

EXAMPLES:
  codectx .                                Analyze current directory
  codectx /path/to/project --verbose       Analyze with verbose output
  codectx plugin add my_plugin.py          Add plugin to default location
  codectx plugin add plugin.py --dir ./custom_dir  Add to custom directory
  codectx plugin remove my_plugin          Remove plugin
  codectx plugin list                      Show all plugins
  codectx plugin list --dir ./custom_dir   Show plugins in custom directory

EOF
}

# Activate venv if exists
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
    echo "[OK] Virtual environment activated"
fi

# No arguments - interactive mode
if [ $# -eq 0 ]; then
    read -p "Enter project path (or press Enter for current): " path
    if [ -z "$path" ]; then
        python3 "$SCRIPT_DIR/main.py" analyze .
    else
        python3 "$SCRIPT_DIR/main.py" analyze "$path"
    fi
    exit 0
fi

# Handle help
if [ "$1" = "help" ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
    exit 0
fi

# Handle plugin subcommand
if [ "$1" = "plugin" ]; then
    if [ -z "$2" ]; then
        echo "[ERROR] Plugin command required: add, remove, or list"
        echo "Usage:"
        echo "  codectx plugin add <file> [--dir <directory>]"
        echo "  codectx plugin remove <name> [--dir <directory>]"
        echo "  codectx plugin list [--dir <directory>]"
        exit 1
    fi

    if [ "$2" = "add" ]; then
        if [ -z "$3" ]; then
            echo "[ERROR] Please specify plugin file path"
            exit 1
        fi
        # Check for --dir option
        if [ "$4" = "--dir" ] && [ -n "$5" ]; then
            python3 "$SCRIPT_DIR/main.py" plugin add "$3" --dir "$5"
        else
            python3 "$SCRIPT_DIR/main.py" plugin add "$3"
        fi
        exit 0
    fi

    if [ "$2" = "remove" ]; then
        if [ -z "$3" ]; then
            echo "[ERROR] Please specify plugin name"
            echo "Usage: codectx plugin remove <name> [--dir <directory>]"
            exit 1
        fi
        if [ "$4" = "--dir" ] && [ -n "$5" ]; then
            python3 "$SCRIPT_DIR/main.py" plugin remove "$3" --dir "$5"
        else
            python3 "$SCRIPT_DIR/main.py" plugin remove "$3"
        fi
        exit 0
    fi

    if [ "$2" = "list" ]; then
        if [ "$3" = "--dir" ] && [ -n "$4" ]; then
            python3 "$SCRIPT_DIR/main.py" plugin list --dir "$4"
        else
            python3 "$SCRIPT_DIR/main.py" plugin list
        fi
        exit 0
    fi

    echo "[ERROR] Unknown plugin command: $2"
    exit 1
fi

# Handle analyze subcommand
if [ "$1" = "analyze" ]; then
    path="${2:-.}"
    shift 2
    python3 "$SCRIPT_DIR/main.py" analyze "$path" "$@"
    exit 0
fi

# Otherwise, treat first argument as path (legacy mode)
path="$1"
shift

echo "[SCAN] Running CodeCtx on: $path"
python3 "$SCRIPT_DIR/main.py" analyze "$path" "$@"
echo "[OK] Analysis complete!"
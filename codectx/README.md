# CodeCtx - Advanced Code Analysis Tool

**CodeCtx** is a powerful code analysis tool that automatically extracts project context including file structures, functions, APIs, dependencies, and more—perfect for feeding into AI models or documentation generation.

## Features

✨ **Smart Code Analysis**
- Extracts functions, APIs, dependencies, and environment variables
- Detects security issues and data flows
- Generates file summaries automatically
- Supports multiple languages

🔌 **Extensible Plugin System**
- Create custom extractors and processors
- Easy plugin management

📦 **Automatic Configuration**
- Auto-initializes on first run
- Platform-specific config directories
- Zero manual setup required

🚀 **Easy Installation**
- Single command installation
- Works on Windows, macOS, Linux

## Installation

### Smart Setup
```bash
cd /path/to/codectx

# Windows
setup.bat

# macOS / Linux
./setup.sh
```

The smart setup bootstraps a local `venv`, installs CodeCtx, creates launchers in `bin/`,
and tries to add that `bin/` directory to your user `PATH`.

### Manual Installation
```bash
pip install -e .
```

After installation, the tool will auto-configure on first run.
You can also invoke it as a module on any platform with `python -m codectx`.

## Quick Start

### Basic Usage
```bash
# Analyze current directory
codectx .

# Equivalent module invocation
python -m codectx .

# Analyze with verbose output
codectx . --verbose

# Analyze specific directory
codectx /path/to/project
```

### Plugin Management
```bash
# List available plugins
codectx plugin list

# Add a custom plugin
codectx plugin add /path/to/my_plugin.py

# Remove a plugin
codectx plugin remove my_plugin
```

## Configuration

On first run, CodeCtx creates a configuration file at:
- **Windows**: `%LOCALAPPDATA%\CodeCtx\config.json`
- **macOS**: `~/.config/codectx/config.json`
- **Linux**: `~/.config/codectx/config.json`

To override the config location on any device, set `CODECTX_CONFIG_DIR`.

Customize the configuration to adjust ignore patterns, output formats, and more.

## Layout

The self-contained project layout is:

```text
C:\tools\codectx
  bin/        # generated command launchers
  src/        # Python package source
  venv/       # local virtual environment
```

## Output

CodeCtx generates a comprehensive JSON file (`project.ctx.json`) containing:
- File tree structure
- Extracted functions and APIs
- Dependencies and imports
- Environment variables
- Detected data flows
- Security issues
- File summaries

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.

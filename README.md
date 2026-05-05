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

### Option 1: Install from source (Development)
```bash
cd /path/to/codectx
pip install -e .
```

### Option 2: Install from package
```bash
pip install codectx
```

After installation, the tool will auto-configure on first run.

## Quick Start

### Basic Usage
```bash
# Analyze current directory
codectx .

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

Customize the configuration to adjust ignore patterns, output formats, and more.

## Output

CodeCtx generates a comprehensive JSON file (`project.ctx.json`) containing:
- File tree structure
- Extracted functions and APIs
- Dependencies and imports
- Environment variables
- Detected data flows
- Security issues
- File summaries

## Architecture

See [README_ARCHITECTURE.md](codectx/README_ARCHITECTURE.md) for detailed module documentation.

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.

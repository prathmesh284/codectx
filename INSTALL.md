# CodeCtx Installation and Setup Guide

## Quick Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation Methods

#### 1. Development Installation (From Source)
Best for development and customization:

```bash
# Clone or download the repository
cd /path/to/codectx

# Install in development mode
pip install -e .
```

#### 2. Standard Installation
For regular use:

```bash
cd /path/to/codectx
pip install .
```

#### 3. Install from Wheel
If you have a built wheel:

```bash
pip install codectx-1.0.0-py3-none-any.whl
```

## First Run - Automatic Configuration

On your first run, CodeCtx automatically initializes:

```bash
codectx .
```

This creates a configuration directory with default settings at:
- **Windows**: `%LOCALAPPDATA%\CodeCtx\config.json`
- **macOS**: `~/.config/codectx/config.json`
- **Linux**: `~/.config/codectx/config.json`

Output shows:
```
Configuration initialized at: C:\Users\YourName\AppData\Local\CodeCtx\config.json
[SCAN] Scanning project at: .
[OK] Found X files
[OK] Output written -> project.ctx.json
```

## Usage After Installation

```bash
# Analyze current directory
codectx .

# Analyze specific path
codectx /path/to/project

# Verbose output
codectx /path/to/project --verbose

# Manage plugins
codectx plugin list
codectx plugin add /path/to/plugin.py
codectx plugin remove plugin_name
```

## Configuration

### Config File Location
Your configuration file is automatically created at:
- **Windows**: `C:\Users\<YourUsername>\AppData\Local\CodeCtx\config.json`
- **macOS**: `/Users/<YourUsername>/.config/codectx/config.json`
- **Linux**: `/home/<YourUsername>/.config/codectx/config.json`

### Default Configuration
```json
{
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
    ".mypy_cache"
  ],
  "ignore_files": [
    ".ctx.json",
    ".DS_Store",
    "*.pyc"
  ],
  "verbose": false,
  "plugins_enabled": true,
  "auto_backup": true
}
```

### Customizing Configuration

Edit the `config.json` file directly to customize settings:

```json
{
  "project_root": "/my/project",
  "output_file": "custom_output.json",
  "ignore_dirs": ["venv", "node_modules", "custom_ignore"],
  "verbose": true
}
```

## Transferring to Another Device

### Option 1: Fresh Installation (Recommended)
1. Install CodeCtx on the new device: `pip install .`
2. Run once to auto-generate config: `codectx .`
3. Customize config as needed

### Option 2: Preserve Configuration
1. Copy your `config.json` to the new device:
   - **From**: `C:\Users\<YourName>\AppData\Local\CodeCtx\config.json`
   - **To**: Same location on new device
2. Install CodeCtx: `pip install .`
3. Configuration will be loaded automatically

### Option 3: Custom Config Directory
Set environment variable to use a specific config directory:

**Windows (PowerShell)**:
```powershell
$env:CODECTX_CONFIG_DIR = "C:\path\to\config"
codectx .
```

**Windows (Command Prompt)**:
```cmd
set CODECTX_CONFIG_DIR=C:\path\to\config
codectx .
```

**macOS/Linux (Bash)**:
```bash
export CODECTX_CONFIG_DIR=/path/to/config
codectx .
```

## Building a Wheel

To distribute CodeCtx as a wheel:

```bash
python -m pip install build
python -m build
```

This creates wheel and source distributions in `dist/` that can be installed on Windows, macOS, or Linux with a supported Python version.

## Troubleshooting

### Command Not Found
If `codectx` command doesn't work:
```bash
# Try running with Python module
python -m codectx .

# Or install in editable mode
pip install -e .
```

### Permission Denied (macOS/Linux)
```bash
# Make sure you have write permissions to config directory
mkdir -p ~/.config/codectx
chmod 755 ~/.config/codectx
```

### Config Not Loading
Check if config file exists:
```bash
# Windows
echo %LOCALAPPDATA%\CodeCtx\config.json

# macOS/Linux
echo ~/.config/codectx/config.json
```

## Uninstallation

```bash
pip uninstall codectx
```

Note: Configuration files are preserved in your user's config directory for future reinstallation.

## For Developers

### Development Setup
```bash
# Clone repository
git clone <repo-url>
cd codectx

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Build distribution
python -m build
```

## Support

For issues and feature requests, please visit: https://github.com/yourusername/codectx/issues

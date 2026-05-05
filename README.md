# CodeCtx

CodeCtx scans a project directory and writes a `project.ctx.json` file with
high-signal context that is useful for AI workflows, code reviews, onboarding,
and lightweight documentation.

## What it does

- Scans a target directory and builds a project context snapshot.
- Extracts file structure, functions, APIs, dependencies, environment hints,
  summaries, and plugin output.
- Writes the result into the directory where you run the command.
- Keeps a single rolling backup in `project.ctx.json.backup`.
- Auto-initializes its config directory on first run.

## Installation

### Option 1: local bootstrap

Use the bundled setup script when you want a self-contained local install with
its own virtual environment and launchers.

```bash
# Windows
setup.bat

# macOS / Linux
./setup.sh
```

The bootstrap script:

- creates `venv/` if needed
- generates launchers in `bin/`
- prefers a user launcher directory already on `PATH`, such as `~/.local/bin`
- attempts to update `PATH` when necessary

### Option 2: standard Python install

```bash
pip install .
```

After publishing to PyPI:

```bash
pip install pycodectx
```

For local development:

```bash
pip install -e .
```

You can also run it directly with:

```bash
python -m codectx .
```

The published package name is `pycodectx`, but the installed CLI command
remains `codectx`.

## Usage

```bash
# Analyze the current directory
codectx .

# Analyze a specific project
codectx /path/to/project

# Show extra detail
codectx . --verbose

# Plugin management
codectx plugin list
codectx plugin add /path/to/plugin.py
codectx plugin remove my_plugin
```

## Output behavior

- `project.ctx.json` is written into the directory you analyze.
- If that file already exists, CodeCtx copies the previous version to
  `project.ctx.json.backup`.
- Only the latest backup is kept.

## Configuration

CodeCtx stores configuration in a per-user directory by default:

- Windows: `%LOCALAPPDATA%\CodeCtx`
- macOS: `~/.config/codectx`
- Linux: `~/.config/codectx`

To override that location, set `CODECTX_CONFIG_DIR`.

Example:

```bash
CODECTX_CONFIG_DIR=/custom/path/codectx
```

The generated `config.json` controls values such as:

- `output_file`
- `ignore_dirs`
- `ignore_files`
- `plugins_enabled`
- `auto_backup`

## Project layout

```text
codectx/
  src/codectx/   Python package
  bin/           generated launchers
  venv/          local virtual environment created by bootstrap
  bootstrap.py   cross-platform setup entry
```

## License

CodeCtx is released under the MIT License. See [LICENSE](LICENSE).

## Support

- Repository: <https://github.com/prathmesh284/codectx>
- Issues: <https://github.com/prathmesh284/codectx/issues>

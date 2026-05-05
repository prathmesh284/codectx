"""Installed deployment helper for CodeCtx."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT_FILES = [
    ".env.example",
    ".gitattributes",
    ".gitignore",
    "LICENSE",
    "MANIFEST.in",
    "README.md",
    "bootstrap.py",
    "pyproject.toml",
    "requirements.txt",
    "setup.bat",
    "setup.py",
    "setup.sh",
]

ENV_TEMPLATE = """# CodeCtx environment template
#
# Only set values here when you want to override the default behavior.
#
# Optional: store CodeCtx config and plugins in a custom directory.
# Windows example:
# CODECTX_CONFIG_DIR=C:\\Users\\your-user\\AppData\\Local\\CodeCtx
#
# macOS / Linux example:
# CODECTX_CONFIG_DIR=/home/your-user/.config/codectx
"""

SETUP_BAT = """@echo off
REM Setup script for CodeCtx on Windows
python bootstrap.py
"""

SETUP_SH = """#!/usr/bin/env sh
# Setup script for CodeCtx on macOS/Linux
python3 bootstrap.py
"""


def main(argv: list[str] | None = None) -> int:
    """Deploy CodeCtx into a dedicated app folder and bootstrap it."""
    parser = argparse.ArgumentParser(
        prog="python -m codectx.setup",
        description="Deploy CodeCtx into a dedicated app folder and bootstrap it.",
    )
    parser.add_argument(
        "--target",
        default=str(default_target_dir()),
        help="Target installation directory",
    )
    args = parser.parse_args(argv)

    target_root = Path(args.target).expanduser().resolve()
    print(f"[INFO] Deploying CodeCtx to: {target_root}")
    deploy_runtime_tree(target_root)
    run_bootstrap(target_root)
    print("[OK] CodeCtx deployment finished.")
    print(f"[OK] App root: {target_root}")
    print(f"[OK] Launcher directory: {target_root / 'bin'}")
    return 0


def default_target_dir() -> Path:
    if sys.platform.startswith("win"):
        return Path("C:/tools/codectx")
    return Path.home() / "tools" / "codectx"


def deploy_runtime_tree(target_root: Path) -> None:
    """Copy the installed runtime into a self-contained app folder."""
    target_root.mkdir(parents=True, exist_ok=True)
    source_root = source_checkout_root()

    if source_root is not None and source_root != target_root:
        sync_source_checkout(source_root, target_root)
        return

    source_package_dir = Path(__file__).resolve().parent
    target_src_dir = target_root / "src" / "codectx"
    if source_package_dir.resolve() != target_src_dir.resolve():
        sync_directory(source_package_dir, target_src_dir)

    bootstrap_module = __import__("bootstrap")
    copy_file(Path(bootstrap_module.__file__).resolve(), target_root / "bootstrap.py")

    write_text_file(target_root / ".env.example", ENV_TEMPLATE)
    write_text_file(target_root / "setup.bat", SETUP_BAT)
    write_text_file(target_root / "setup.sh", SETUP_SH, executable=True)


def source_checkout_root() -> Path | None:
    """Return the source checkout root when running from a repo checkout."""
    candidate = Path(__file__).resolve().parents[2]
    if (candidate / "pyproject.toml").exists() and (candidate / "bootstrap.py").exists():
        return candidate
    return None


def sync_source_checkout(source_root: Path, target_root: Path) -> None:
    """Deploy a source checkout while skipping generated local artifacts."""
    sync_directory(source_root / "src", target_root / "src")
    sync_optional_directory(source_root / ".github", target_root / ".github")

    for filename in PROJECT_ROOT_FILES:
        copy_file(source_root / filename, target_root / filename)


def sync_directory(source_dir: Path, target_dir: Path) -> None:
    """Replace a target directory with a clean copy of the source."""
    if target_dir.exists():
        shutil.rmtree(target_dir)

    shutil.copytree(
        source_dir,
        target_dir,
        ignore=shutil.ignore_patterns(
            "__pycache__",
            "*.pyc",
            "*.pyo",
        ),
    )


def sync_optional_directory(source_dir: Path, target_dir: Path) -> None:
    """Copy an optional directory if it exists in the source checkout."""
    if source_dir.exists():
        sync_directory(source_dir, target_dir)


def copy_file(source_file: Path, target_file: Path) -> None:
    """Copy one file into the target tree."""
    if not source_file.exists():
        return
    if source_file.resolve() == target_file.resolve():
        return
    target_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, target_file)


def write_text_file(
    target_file: Path, content: str, executable: bool = False
) -> None:
    """Write a generated helper file into the target tree."""
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(content, encoding="utf-8")
    if executable:
        try:
            target_file.chmod(0o755)
        except OSError:
            pass


def run_bootstrap(target_root: Path) -> None:
    """Run bootstrap inside the deployed application folder."""
    subprocess.run(
        [sys.executable, str(target_root / "bootstrap.py")],
        cwd=target_root,
        check=True,
    )


if __name__ == "__main__":
    raise SystemExit(main())

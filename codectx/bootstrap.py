#!/usr/bin/env python3
"""Smart cross-platform bootstrap for the self-contained CodeCtx project."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / "venv"
BIN_DIR = PROJECT_ROOT / "bin"
WINDOWS = os.name == "nt"


def main() -> int:
    print(f"[INFO] Project root: {PROJECT_ROOT}")
    ensure_env_file()
    ensure_virtualenv()
    python_bin = get_venv_python()
    install_project(python_bin)
    create_launchers(python_bin)
    configure_path()
    warm_up_cli(python_bin)
    print(f"[OK] Setup finished. Launchers are in: {BIN_DIR}")
    return 0


def ensure_env_file() -> None:
    env_file = PROJECT_ROOT / ".env"
    env_example = PROJECT_ROOT / ".env.example"
    if not env_file.exists() and env_example.exists():
        shutil.copyfile(env_example, env_file)
        print("[OK] Created .env from .env.example")


def ensure_virtualenv() -> None:
    if VENV_DIR.exists():
        print("[OK] Virtual environment already exists")
        return
    print("[INFO] Creating virtual environment")
    run([sys.executable, "-m", "venv", str(VENV_DIR)])


def get_venv_python() -> Path:
    python_bin = (
        VENV_DIR / "Scripts" / "python.exe"
        if WINDOWS
        else VENV_DIR / "bin" / "python"
    )
    if not python_bin.exists():
        raise FileNotFoundError(f"Virtual environment python not found: {python_bin}")
    return python_bin


def install_project(python_bin: Path) -> None:
    print("[INFO] Installing CodeCtx into the local virtual environment")
    try:
        run(
            [
                str(python_bin),
                "-m",
                "pip",
                "install",
                "--upgrade",
                "pip",
                "setuptools",
                "wheel",
            ]
        )
    except subprocess.CalledProcessError:
        print("[WARN] Skipping packaging-tool upgrade; continuing with local install")

    run(
        [
            str(python_bin),
            "-m",
            "pip",
            "install",
            "--no-build-isolation",
            "-e",
            str(PROJECT_ROOT),
        ]
    )


def create_launchers(python_bin: Path) -> None:
    BIN_DIR.mkdir(exist_ok=True)
    create_windows_launchers(python_bin)
    create_posix_launcher(python_bin)


def create_windows_launchers(python_bin: Path) -> None:
    cmd_launcher = BIN_DIR / "codectx.cmd"
    ps1_launcher = BIN_DIR / "codectx.ps1"
    cmd_launcher.write_text(
        "@echo off\n"
        'set "CODECTX_PROJECT_ROOT=%~dp0.."\n'
        f'"{python_bin}" -m codectx %*\n',
        encoding="utf-8",
    )
    ps1_launcher.write_text(
        "$ProjectRoot = Split-Path -Parent $PSScriptRoot\n"
        f'& "{python_bin}" -m codectx @args\n',
        encoding="utf-8",
    )


def create_posix_launcher(python_bin: Path) -> None:
    posix_launcher = BIN_DIR / "codectx"
    posix_launcher.write_text(
        "#!/usr/bin/env sh\n"
        'PROJECT_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"\n'
        f'"{python_bin}" -m codectx "$@"\n',
        encoding="utf-8",
    )
    try:
        posix_launcher.chmod(0o755)
    except OSError:
        pass


def configure_path() -> None:
    if WINDOWS:
        add_windows_path(BIN_DIR)
    else:
        add_posix_path(BIN_DIR)


def add_windows_path(bin_dir: Path) -> None:
    current = os.environ.get("PATH", "")
    bin_text = str(bin_dir)
    if bin_text.lower() in current.lower():
        print("[OK] bin directory already available in current PATH")
        return

    powershell = shutil.which("powershell") or shutil.which("pwsh")
    if powershell is None:
        print(f"[WARN] Could not update user PATH automatically. Add this manually: {bin_text}")
        return

    script = (
        "$path = [Environment]::GetEnvironmentVariable('Path', 'User');"
        f"$bin = '{bin_text}';"
        "if (-not $path) { $path = $bin } "
        "elseif ($path -notlike \"*\" + $bin + \"*\") { $path = $path + ';' + $bin };"
        "[Environment]::SetEnvironmentVariable('Path', $path, 'User')"
    )
    try:
        run([powershell, "-NoProfile", "-Command", script])
        print(f"[OK] Added {bin_text} to user PATH")
    except subprocess.CalledProcessError:
        print(f"[WARN] Could not update user PATH automatically. Add this manually: {bin_text}")


def add_posix_path(bin_dir: Path) -> None:
    shell = Path(os.environ.get("SHELL", ""))
    if shell.name == "zsh":
        rc_file = Path.home() / ".zshrc"
    elif shell.name == "bash":
        rc_file = Path.home() / ".bashrc"
    else:
        rc_file = Path.home() / ".profile"

    export_line = f'export PATH="{bin_dir}:$PATH"'
    existing = rc_file.read_text(encoding="utf-8") if rc_file.exists() else ""
    if export_line in existing:
        print(f"[OK] bin directory already configured in {rc_file}")
        return
    with rc_file.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(f"\n# CodeCtx local launcher\n{export_line}\n")
    print(f"[OK] Added bin directory to {rc_file}")


def warm_up_cli(python_bin: Path) -> None:
    run([str(python_bin), "-m", "codectx", "--help"], env=project_env())


def project_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("CODECTX_CONFIG_DIR", str(PROJECT_ROOT / ".config"))
    return env


def run(command: list[str], env: dict[str, str] | None = None) -> None:
    subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env=env,
        check=True,
    )


if __name__ == "__main__":
    raise SystemExit(main())

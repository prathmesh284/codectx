#!/usr/bin/env python3
"""Smart cross-platform bootstrap for the self-contained CodeCtx project."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SOURCE_DIR = PROJECT_ROOT / "src"
VENV_DIR = PROJECT_ROOT / "venv"
BIN_DIR = PROJECT_ROOT / "bin"
WINDOWS = os.name == "nt"


def main() -> int:
    print(f"[INFO] Project root: {PROJECT_ROOT}")
    ensure_env_file()
    ensure_virtualenv()
    python_bin = get_venv_python()
    validate_runtime(python_bin)
    launcher_dirs = create_launchers(python_bin)
    configure_path(launcher_dirs)
    warm_up_cli(python_bin)
    print("[OK] Setup finished.")
    for launcher_dir in launcher_dirs:
        print(f"[OK] Launcher available in: {launcher_dir}")
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


def validate_runtime(python_bin: Path) -> None:
    print("[INFO] Preparing the local virtual environment")
    if runtime_dependencies_available(python_bin):
        print("[OK] Optional runtime dependencies are available")
    else:
        print("[WARN] Optional package 'python-dotenv' is not installed; continuing without it")


def runtime_dependencies_available(python_bin: Path) -> bool:
    command = [str(python_bin), "-c", "import dotenv"]
    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env=project_env(),
        check=False,
        capture_output=True,
    )
    return result.returncode == 0


def create_launchers(python_bin: Path) -> list[Path]:
    launcher_dirs = [BIN_DIR]
    BIN_DIR.mkdir(exist_ok=True)
    create_windows_launchers(python_bin)
    create_posix_launcher(python_bin)
    user_bin = preferred_user_bin_dir()
    if user_bin is not None:
        try:
            user_bin.mkdir(parents=True, exist_ok=True)
            create_windows_launchers(python_bin, user_bin)
            create_posix_launcher(python_bin, user_bin)
            launcher_dirs.insert(0, user_bin)
        except OSError:
            print(f"[WARN] Could not write launcher into preferred user bin: {user_bin}")
    return launcher_dirs


def create_windows_launchers(
    python_bin: Path, target_dir: Path | None = None
) -> None:
    target_dir = target_dir or BIN_DIR
    cmd_launcher = target_dir / "codectx.cmd"
    ps1_launcher = target_dir / "codectx.ps1"
    cmd_launcher.write_text(
        "@echo off\n"
        f'set "PYTHONPATH={SOURCE_DIR}"\n'
        f'"{python_bin}" -m codectx %*\n'
        "exit /b %ERRORLEVEL%\n",
        encoding="utf-8",
    )
    ps1_launcher.write_text(
        f'$env:PYTHONPATH = "{SOURCE_DIR}"' "\n"
        f'& "{python_bin}" -m codectx @args\n'
        "exit $LASTEXITCODE\n",
        encoding="utf-8",
    )


def create_posix_launcher(
    python_bin: Path, target_dir: Path | None = None
) -> None:
    target_dir = target_dir or BIN_DIR
    posix_launcher = target_dir / "codectx"
    posix_launcher.write_text(
        "#!/usr/bin/env sh\n"
        f'export PYTHONPATH="{SOURCE_DIR}"\n'
        f'"{python_bin}" -m codectx "$@"\n',
        encoding="utf-8",
    )
    try:
        posix_launcher.chmod(0o755)
    except OSError:
        pass


def preferred_user_bin_dir() -> Path | None:
    home = Path.home()
    if WINDOWS:
        candidates = [home / ".local" / "bin"]
    else:
        candidates = [home / ".local" / "bin", home / "bin"]

    active_path_entries = current_path_entries()
    for candidate in candidates:
        if str(candidate).lower() in active_path_entries:
            return candidate
    return candidates[0] if candidates else None


def configure_path(launcher_dirs: list[Path]) -> None:
    for launcher_dir in launcher_dirs:
        if path_contains(launcher_dir):
            print(f"[OK] Launcher directory already on PATH: {launcher_dir}")
            return

    target_dir = launcher_dirs[0]
    if WINDOWS:
        add_windows_path(target_dir)
    else:
        add_posix_path(target_dir)


def current_path_entries() -> set[str]:
    entries: set[str] = set()
    for path_name in ("PATH", "Path"):
        path_value = os.environ.get(path_name, "")
        for entry in path_value.split(os.pathsep):
            entry = entry.strip()
            if entry:
                entries.add(entry.lower())
    return entries


def path_contains(path_dir: Path) -> bool:
    path_text = str(path_dir).lower()
    if path_text in current_path_entries():
        return True
    if WINDOWS:
        return path_text in get_windows_user_path_entries()
    return path_configured_in_shell(path_dir)


def get_windows_user_path_entries() -> set[str]:
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
            try:
                stored_path = winreg.QueryValueEx(key, "Path")[0]
            except FileNotFoundError:
                stored_path = ""
    except OSError:
        return set()

    return {
        entry.strip().lower()
        for entry in stored_path.split(";")
        if entry.strip()
    }


def add_windows_path(bin_dir: Path) -> None:
    bin_text = str(bin_dir)
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_READ | winreg.KEY_SET_VALUE,
        ) as key:
            try:
                stored_path = winreg.QueryValueEx(key, "Path")[0]
            except FileNotFoundError:
                stored_path = ""

            entries = [entry.strip() for entry in stored_path.split(";") if entry.strip()]
            if not any(entry.lower() == bin_text.lower() for entry in entries):
                entries.append(bin_text)
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, ";".join(entries))
        print(f"[OK] Added {bin_text} to user PATH")
    except OSError:
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


def path_configured_in_shell(bin_dir: Path) -> bool:
    shell = Path(os.environ.get("SHELL", ""))
    if shell.name == "zsh":
        rc_file = Path.home() / ".zshrc"
    elif shell.name == "bash":
        rc_file = Path.home() / ".bashrc"
    else:
        rc_file = Path.home() / ".profile"
    if not rc_file.exists():
        return False
    return str(bin_dir) in rc_file.read_text(encoding="utf-8")


def warm_up_cli(python_bin: Path) -> None:
    run([str(python_bin), "-m", "codectx", "--help"], env=project_env())


def project_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SOURCE_DIR)
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

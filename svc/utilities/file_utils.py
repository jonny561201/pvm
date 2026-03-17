import os
import shutil
import sys
from pathlib import Path

from svc.constants.file_constants import File, OS


def set_global_version_file(version: str):
    version_file = File.BIN_DIR / "global-version"
    with open(version_file, 'w') as f:
        f.write(version)


def get_global_version() -> str:
    version_file = File.BIN_DIR / "global-version"
    if not version_file.is_file():
        return '--- Not found ---'

    with open(version_file, 'r') as f:
        return f.read().strip()


def copy_python_executables_windows(folder: Path):
    python_path = folder / 'python'
    dest_path = File.DEFAULT_DIR
    shutil.copytree(python_path, dest_path, dirs_exist_ok=True)


def set_symlink_unix(folder: Path, executable: str):
    target = _get_executable(folder, executable)
    executable_loc = File.DEFAULT_DIR / executable
    tmp_link = executable_loc.with_suffix(".tmp")

    if tmp_link.exists() or tmp_link.is_symlink():
        tmp_link.unlink()

    os.symlink(target, tmp_link)
    os.replace(tmp_link, executable_loc)


def _get_executable(folder: Path, executable: str) -> Path:
    python = folder / 'python' / 'bin' / executable

    if not python.is_file() or python is None:
        sys.exit(f"Unable to locate {executable} executable in {folder}")
    return python

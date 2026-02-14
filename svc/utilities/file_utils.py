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

    return folder.name


def set_python_symlink_unix(folder: Path):
    target = _get_python_executable(folder)
    tmp_link = File.CURRENT_PYTHON.with_suffix(".tmp")

    if tmp_link.exists() or tmp_link.is_symlink():
        tmp_link.unlink()

    os.symlink(target, tmp_link)
    os.replace(tmp_link, File.CURRENT_PYTHON)

    return folder.name


def _get_python_executable(folder: Path) -> Path:
    python = folder / 'python' / 'python.exe' if OS.detect() == OS.WINDOWS else folder / 'python' / 'bin' / 'python'

    if not python.is_file() or python is None:
        sys.exit(f"Unable to locate python executable in {folder}")
    return python

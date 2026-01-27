import re
import sys
from pathlib import Path
import os

from svc.constants.file_constants import FileMode, File


def create_pvm_directory():
    pvm_dir = Path.home() / ".pvm"
    pvm_dir.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(pvm_dir, FileMode.READ_WRITE_EXEC)
    except PermissionError:
        pass
    return pvm_dir


def create_version_directory(release: str):
    version = _get_full_version(release)
    os.makedirs(File.VERSION_DIR / version, exist_ok=True)

    return version


def get_python_version_folders() -> list[Path]:
    pvm_dir = File.VERSION_DIR
    if not pvm_dir.exists():
        return []

    version_folders = []
    for item in pvm_dir.iterdir():
        if item.is_dir() and item.name.startswith("python-"):
            version_folders.append(item)

    return version_folders


def set_global_python(version: str) -> str:
    folders = get_python_version_folders()
    folder = next((folder for folder in folders if version in folder.name) , None)
    if not folder:
        raise ValueError(f"python {version} is not installed")
    target = _get_python_executable(folder.name)
    tmp_link = File.CURRENT_PYTHON.with_suffix(".tmp")

    if tmp_link.exists() or tmp_link.is_symlink():
        tmp_link.unlink()

    os.symlink(target, tmp_link)
    os.replace(tmp_link, File.CURRENT_PYTHON)

    return folder.name


def _get_full_version(url: str):
    pattern = r"cpython-(\d+)\.(\d+)\.(\d+)(?=(?:\+|%2B)\d+)"

    m = re.search(pattern, url)
    if not m:
        raise ValueError("No Python version found")

    major, minor, patch = m.groups()
    return f"python-{major}.{minor}.{patch}"


def _get_python_executable(folder: str) -> Path:
    python = File.VERSION_DIR / folder / 'python' / 'bin' / 'python'
    if not python.is_file():
        sys.exit(f"python {folder} is not installed")
    return python

import re
import sys
from pathlib import Path
import os

from svc.constants.file_constants import FileMode, File, OS


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
    version_dir = File.VERSION_DIR
    if not version_dir.exists():
        return []

    return list(filter(lambda folder: folder.is_dir() and folder.name.startswith("python-"), version_dir.iterdir()))


def find_python_version(version: str):
    version_dir = File.VERSION_DIR
    if not version_dir.exists():
        sys.exit(f"python {version} is not installed")

    for item in version_dir.iterdir():
        if item.is_dir() and version in item.name:
            return item.name
    sys.exit(f"python {version} is not installed")


def set_global_python(version: str) -> str:
    folders = get_python_version_folders()
    folder = next((folder for folder in folders if version in folder.name) , None)
    if not folder:
        sys.exit(f"python {version} is not installed")

    target = _get_python_executable(folder.name)
    tmp_link = File.CURRENT_PYTHON.with_suffix(".tmp")

    if tmp_link.exists() or tmp_link.is_symlink():
        tmp_link.unlink()

    os.symlink(target, tmp_link)
    os.replace(tmp_link, File.CURRENT_PYTHON)

    return folder.name

def ensure_version_not_installed(version: str):
    directories = get_python_version_folders()
    folder = next((folder for folder in directories if folder.name.startswith(f'python-{version}')), None)
    if folder:
        sys.exit(f"python {version} is not installed")


def _get_full_version(url: str):
    pattern = r"cpython-(\d+)\.(\d+)\.(\d+)(?=(?:\+|%2B)\d+)"

    m = re.search(pattern, url)
    if not m:
        sys.exit("No Python version found to create python version folder")

    major, minor, patch = m.groups()
    return f"python-{major}.{minor}.{patch}"


def _get_python_executable(folder: str) -> Path:
    python = File.VERSION_DIR / folder / 'python' if OS.detect() == OS.WINDOWS else File.VERSION_DIR / folder / 'python' / 'bin' / 'python'

    if not python.is_file() or python is None:
        sys.exit(f"{folder} is not installed")
    return python

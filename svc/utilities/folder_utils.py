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


def get_python_version_folders(pvm_dir: Path) -> list[Path]:
    if not pvm_dir.exists():
        return []

    version_folders = []
    for item in pvm_dir.iterdir():
        if item.is_dir() and item.name.startswith("python-"):
            version_folders.append(item)

    return version_folders


def set_global_python(version: str):
    target = _get_python_executable(version)
    tmp_link = File.CURRENT_PYTHON.with_suffix(".tmp")

    if tmp_link.exists() or tmp_link.is_symlink():
        tmp_link.unlink()

    os.symlink(target, tmp_link)
    os.replace(tmp_link, File.CURRENT_PYTHON)


def _get_full_version(url: str):
    pattern = r"cpython-(\d+)\.(\d+)\.(\d+)(?=(?:\+|%2B)\d+)"

    m = re.search(pattern, url)
    if not m:
        raise ValueError("No Python version found")

    major, minor, patch = m.groups()
    return f"python-{major}.{minor}.{patch}"


def _get_python_executable(version: str) -> Path:
    python = File.VERSION_DIR / f'Python-{version}' / 'bin' / 'python'
    if not python.is_file():
        sys.exit(f"python {version} is not installed")
    return python

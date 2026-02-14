import os
import re
import sys
from pathlib import Path

from svc.constants.file_constants import File


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
    for item in File.VERSION_DIR.iterdir():
        if item.is_dir() and version in item.name:
            return item.name
    return None


def ensure_version_not_installed(version: str):
    directories = get_python_version_folders()
    folder = next((folder for folder in directories if folder.name.startswith(f'python-{version}')), None)
    if folder:
        sys.exit(f"python {version} is not installed")


def _get_full_version(url: str):
    pattern = r"cpython-(\d+)\.(\d+)\.(\d+)(?=(?:\+|%2B)\d+)"
    matches = re.search(pattern, url)
    if not matches:
        sys.exit("No Python version found to create python version folder")

    major, minor, patch = matches.groups()
    return f"python-{major}.{minor}.{patch}"

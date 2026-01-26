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


def delete_tar_file(pvm_dir: Path, filename: str):
    file_path = pvm_dir / filename
    if file_path.exists():
        file_path.unlink()


def get_python_version_folders(pvm_dir: Path) -> list[Path]:
    if not pvm_dir.exists():
        return []

    version_folders = []
    for item in pvm_dir.iterdir():
        if item.is_dir() and item.name.startswith("Python-"):
            version_folders.append(item)

    return version_folders


def get_python_executable(version: str) -> Path:
    python = File.CURRENT_PYTHON
    if not python.is_file():
        sys.exit(f"pvm: python {version} is not installed")
    return python


def set_global_python(version: str):
    target = get_python_executable(version)
    tmp_link = File.CURRENT_PYTHON.with_suffix(".tmp")

    if tmp_link.exists() or tmp_link.is_symlink():
        tmp_link.unlink()

    os.symlink(target, tmp_link)

    os.replace(tmp_link, File.CURRENT_PYTHON)

    print(f"pvm: global python set to {version}")
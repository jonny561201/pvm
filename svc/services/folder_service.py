from pathlib import Path
import os

from svc.constants.file_constants import FileMode


def create_pvm_directory():
    pvm_dir = Path.home() / ".pvm"
    pvm_dir.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(pvm_dir, FileMode.read_write_exec)
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
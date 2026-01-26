from pathlib import Path
import os

from svc.constants.file_constants import File


def create_pvm_directory():
    pvm_dir = Path.home() / ".pvm"
    pvm_dir.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(pvm_dir, File.read_write_exec)
    except PermissionError:
        pass
    return pvm_dir


def delete_tar_file(pvm_dir: Path, filename: str):
    file_path = pvm_dir / filename
    if file_path.exists():
        file_path.unlink()
from pathlib import Path


def delete_tar_file(pvm_dir: Path, filename: str):
    file_path = pvm_dir / filename
    if file_path.exists():
        file_path.unlink()
import os
import tarfile
from pathlib import Path

from svc.utilities.requests import requests


def download_python_release(url: str, pvm_dir: Path, file_name: str):
    print('...downloading python version...')
    pvm_dir.mkdir(parents=True, exist_ok=True)
    out_path = pvm_dir / file_name
    tmp_path = out_path.with_suffix(out_path.suffix + ".part")

    headers = {"User-Agent": "pvm-installer/1.0"}
    with requests.get(url, headers=headers, stream=True, timeout=30) as resp:
        resp.raise_for_status()
        with open(tmp_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=64 * 1024):
                if chunk:
                    f.write(chunk)

    os.replace(tmp_path, out_path)


def extract_zip(zip_path: Path, filename: str):
    print('...extracting python version...')
    file_path = zip_path / filename
    with tarfile.open(file_path, "r:*") as tf:
        tf.extractall(zip_path)


def delete_tar_file(pvm_dir: Path, filename: str):
    file_path = pvm_dir / filename
    if file_path.exists():
        file_path.unlink()

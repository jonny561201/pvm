import os
import shutil
import tarfile
from pathlib import Path

import requests

from svc.constants.file_constants import File

pvm_dir = Path.home() / ".pvm"

def download_python(version: str):
    name = f"Python-{version}.tgz"
    url = f"https://www.python.org/ftp/python/{version}/{name}"

    pvm_dir.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(pvm_dir, File.read_write_exec)
    except PermissionError:
        pass

    out_path = pvm_dir / name
    tmp_path = out_path.with_suffix(out_path.suffix + ".part")

    headers = {"User-Agent": "pvm-installer/1.0"}
    with requests.get(url, headers=headers, stream=True, timeout=30) as resp:
        resp.raise_for_status()
        with open(tmp_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=64 * 1024):
                if chunk:
                    f.write(chunk)

    os.replace(tmp_path, out_path)

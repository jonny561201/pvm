import os
import shutil
import tarfile
from functools import partial
from pathlib import Path
from typing import List

import requests

from svc.constants.file_constants import FileMode, OS, Architecture


def get_python_release_tag():
    url = 'https://raw.githubusercontent.com/indygreg/python-build-standalone/latest-release/latest-release.json'
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    return data.get("tag")

def get_python_releases(tag: str):
    if tag is None:
        raise Exception("Unable to list of latest python releases")
    url = f'https://api.github.com/repos/astral-sh/python-build-standalone/releases/tags/{tag}'
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    return data.get("assets", [])


def filter_python_release(releases: List[dict], os: str, arch: str):
    filtered_releases = list(filter(partial(__asset_match, os, arch), releases))
    return [asset.get('browser_download_url') for asset in filtered_releases]


def __asset_match(os: str, arch: str, asset: dict, ):
    name = asset.get("name")
    return os in name and arch in name and 'install_only.tar.gz' in name


def download_python(pvm_dir: Path, version: str, file_name: str):
    url = f"https://www.python.org/ftp/python/{version}/{file_name}"

    pvm_dir.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(pvm_dir, FileMode.READ_WRITE_EXEC)
    except PermissionError:
        pass

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
    file_path = zip_path / filename
    with tarfile.open(file_path, "r:*") as tf:
        for member in tf.getmembers():
            member_name = member.name
            if not member_name:
                continue

            target_path = (zip_path / member_name).resolve()

            if member.isdir():
                target_path.mkdir(parents=True, exist_ok=True)
            else:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                src = tf.extractfile(member)
                if src is None:
                    continue
                with src, open(target_path, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                try:
                    os.chmod(target_path, member.mode)
                except Exception:
                    pass

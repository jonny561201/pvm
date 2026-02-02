from typing import List

from svc.utilities.requests import requests


def get_python_release_tag():
    print('...getting python releases...')
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


def find_python_release(releases: List[dict], version: str, os: str, arch: str):
    match = next((asset.get("browser_download_url") for asset in releases if __asset_match(version, os, arch, asset)), None)
    if not match:
        raise Exception(f"Unable to find python release for version {version}")
    return match


def __asset_match(version: str, os: str, arch: str, asset: dict, ):
    name = asset.get("name")
    return os in name and arch in name and 'install_only.tar.gz' in name and version in name

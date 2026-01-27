from functools import partial
from typing import List

import requests


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


def filter_python_release(releases: List[dict], os: str, arch: str):
    filtered_releases = list(filter(partial(__asset_match, os, arch), releases))
    return [asset.get('browser_download_url') for asset in filtered_releases]


def __asset_match(os: str, arch: str, asset: dict, ):
    name = asset.get("name")
    return os in name and arch in name and 'install_only.tar.gz' in name

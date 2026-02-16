import os
import re
from pathlib import Path

from svc.constants.file_constants import Architecture, OS
from svc.utilities.folder_utils import ensure_version_not_installed
from svc.utilities.prebuilt_release_utils import get_python_release_tag, get_python_releases, find_python_release


def find_matching_release(version: str):
    ensure_version_not_installed(version)
    tag = get_python_release_tag()
    releases = get_python_releases(tag)

    return find_python_release(releases, version, OS.detect(), Architecture.detect())


def update_paths(new_version: Path):
    separator = os.pathsep  # ':' on mac/Linux, ';' on Windows
    paths = os.environ.get('PATH')
    updated_path = _remove_existing_versions_from_path(paths, separator)

    new_version_str = str(new_version.absolute()).replace("\\", "/")
    segments = [new_version_str] + updated_path.split(separator)
    safe_segments = [f'"{s}"' for s in segments]

    return separator.join(safe_segments)


def _remove_existing_versions_from_path(paths: str, sep: str) -> str:
    pattern = rf"(?:^{sep}|{sep})[^ {sep}]*[.]pvm[/\\]versions[/\\]python-[^ {sep}:]+(?:[/\\]python)?(?:[/\\]bin)?"
    paths = re.sub(pattern, "", paths)
    paths = re.sub(rf"{sep}{{2,}}", sep, paths)

    return paths.strip(sep)

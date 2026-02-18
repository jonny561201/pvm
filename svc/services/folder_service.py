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


def update_paths(new_version: Path) -> str:
    sep = os.pathsep
    paths = os.environ.get('PATH', '')
    cleaned_path = _remove_existing_versions_from_path(paths)
    updated_path = [str(new_version.absolute())] + cleaned_path.split(sep)
    segments = [p for p in updated_path if p]

    if OS.detect() == OS.WINDOWS:
        segments = [_win_to_msys(item) for item in segments]

    return ":".join(segments)


def _remove_existing_versions_from_path(paths: str) -> str:
    sep = ":"
    pattern = r"(?:^|:)[^:]*[\\/]\.pvm[\\/]+versions[\\/]+python-[^\\/:\s]+(?:[\\/]+python)?(?:[\\/]+bin)?"
    paths = re.sub(pattern, "", paths, flags=re.VERBOSE)
    paths = re.sub(r":{2,}", ":", paths)

    return paths.strip(sep)


def _win_to_msys(path: str) -> str:
    p = Path(path)
    drive = p.drive.rstrip(":").lower()
    rest = p.as_posix().split(":", 1)[-1]

    return f"/{drive}{rest}"

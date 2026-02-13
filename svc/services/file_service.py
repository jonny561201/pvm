import sys

from svc.constants.file_constants import OS
from svc.utilities.file_utils import copy_python_executables_windows, set_python_symlink_unix
from svc.utilities.folder_utils import get_python_version_folders


def set_global_python(version: str) -> str:
    folders = get_python_version_folders()
    folder = next((folder for folder in folders if version in folder.name) , None)
    if not folder:
        sys.exit(f"python {version} is not installed")

    if OS.detect() == OS.WINDOWS:
        return copy_python_executables_windows(folder)

    return set_python_symlink_unix(folder)


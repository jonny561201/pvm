import os
import sys

from svc.constants.file_constants import OS, File
from svc.utilities.file_utils import copy_python_executables_windows, set_python_symlink_unix, get_global_version
from svc.utilities.folder_utils import get_python_version_folders
from svc.utilities.install_utils import download_python_release, extract_zip, delete_tar_file


def set_global_python(version: str) -> str:
    folders = get_python_version_folders()
    folder = next((folder for folder in folders if version in folder.name) , None)
    if not folder:
        sys.exit(f"python {version} is not installed")

    if OS.detect() == OS.WINDOWS:
        return copy_python_executables_windows(folder)

    return set_python_symlink_unix(folder)


def get_active_python_version() -> str:
    global_ver = get_global_version()
    instance_ver = os.environ.get('PVM_VERSION')

    if instance_ver is not None and instance_ver.strip() != '':
        return instance_ver

    return global_ver


def download_extract_binaries(file_name: str, folder_name: str, release: str):
    directory = File.VERSION_DIR / folder_name
    download_python_release(release, directory, file_name)
    extract_zip(directory, file_name)
    delete_tar_file(directory, file_name)

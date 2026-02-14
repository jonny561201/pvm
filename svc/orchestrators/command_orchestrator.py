import sys

from svc.constants.file_constants import File
from svc.services.file_service import set_global_python, get_active_python_version, download_extract_binaries
from svc.services.folder_service import find_matching_release, update_paths
from svc.utilities.file_utils import set_global_version_file
from svc.utilities.folder_utils import get_python_version_folders, create_version_directory, find_python_version


def install_latest_release(version: str):
    release = find_matching_release(version)
    file_name = f"{version}.tgz"
    folder_name = create_version_directory(release)
    download_extract_binaries(file_name, folder_name, release)


def list_python_versions():
    directories = get_python_version_folders()
    versions = sorted([directory.name for directory in directories])
    active_version = get_active_python_version()
    for version in versions:
        print(f" {'*' if active_version in version else ' '} {version}")
    if len(versions) == 0:
        print("No Python versions installed.")


def set_default_version(version: str):
    version_folder = set_global_python(version)
    stripped_version = version_folder.replace('python-', '')
    set_global_version_file(stripped_version)
    print(f"pvm: global python set to {version_folder}")


def use_python_version(version: str):
    folder = find_python_version(version)
    executable = File.VERSION_DIR / folder / 'python' / 'bin'
    new_path = update_paths(executable)

    print(f"export PATH={new_path}")
    print(f'export PVM_VERSION="{folder}"')
    print(f"pvm: using python version {folder}", file=sys.stderr)

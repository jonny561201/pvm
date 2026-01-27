from svc.constants.file_constants import File
from svc.utilities.folder_utils import get_python_version_folders, set_global_python, delete_tar_file
from svc.utilities.install_utils import download_python, extract_zip


def install_orchestration(version: str):
    file_name = f"{version}.tgz"
    print('...downloading python version...')
    download_python(File.VERSION_DIR, version, file_name)
    print('...extracting python version...')
    extract_zip(File.VERSION_DIR, file_name)
    delete_tar_file(File.VERSION_DIR, file_name)


def get_python_versions():
    directories = get_python_version_folders(File.VERSION_DIR)
    versions = sorted([directory.name for directory in directories])
    for version in versions:
        print(version)


def set_default_version(version: str):
    set_global_python(version)
    print(f"pvm: global python set to {version}")

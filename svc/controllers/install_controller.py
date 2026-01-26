from pathlib import Path

from svc.services.folder_service import delete_tar_file, get_python_version_folders
from svc.services.install_service import download_python, extract_zip


def install_orchestration(version: str):
    pvm_dir = Path.home() / ".pvm"
    file_name = f"Python-{version}.tgz"
    print('...downloading python version...')
    download_python(pvm_dir, version, file_name)
    print('...extracting python version...')
    extract_zip(pvm_dir, file_name)
    delete_tar_file(pvm_dir, file_name)


def get_python_versions():
    pvm_dir = Path.home() / ".pvm"
    directories = get_python_version_folders(pvm_dir)
    versions = sorted([directory.name for directory in directories])
    for version in versions:
        print(version)

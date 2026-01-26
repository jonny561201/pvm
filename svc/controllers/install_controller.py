from svc.constants.file_constants import File
from svc.services.folder_service import delete_tar_file, get_python_version_folders
from svc.services.install_service import download_python, extract_zip


def install_orchestration(version: str):
    file_name = f"{version}.tgz"
    print('...downloading python version...')
    download_python(File.VERSION_DIR, version, file_name)
    print('...extracting python version...')
    extract_zip(File.VERSION_DIR, file_name)
    delete_tar_file(File.VERSION_DIR, file_name)


def get_python_versions():
    directories = get_python_version_folders(File.PVM_DIR)
    versions = sorted([directory.name for directory in directories])
    for version in versions:
        print(version)

from pathlib import Path

from svc.services.folder_service import delete_tar_file
from svc.services.install_service import download_python, extract_zip


def install_orchestration(version: str):
    pvm_dir = Path.home() / ".pvm"
    file_name = f"Python-{version}.tgz"
    print('...downloading python version...')
    download_python(pvm_dir, version, file_name)
    print('...extracting python version...')
    extract_zip(pvm_dir, file_name)
    delete_tar_file(pvm_dir, file_name)


install_orchestration('3.11.4')
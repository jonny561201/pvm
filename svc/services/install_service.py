from svc.constants.file_constants import File, Architecture, OS
from svc.utilities.folder_utils import get_python_version_folders, set_global_python, create_version_directory
from svc.utilities.install_utils import download_python_release, extract_zip, delete_tar_file
from svc.utilities.prebuilt_release_utils import get_python_release_tag, get_python_releases, filter_python_release


def install_latest_release(version: str):
    tag = get_python_release_tag()
    releases = get_python_releases(tag)
    release = filter_python_release(releases, version, OS.APPLE, Architecture.INTEL)
    file_name = f"{version}.tgz"
    folder_name = create_version_directory(release[0])
    directory = File.VERSION_DIR / folder_name
    download_python_release(release[0], directory, file_name)
    extract_zip(directory, file_name)
    delete_tar_file(directory, file_name)


def get_python_versions():
    directories = get_python_version_folders()
    versions = sorted([directory.name for directory in directories])
    for version in versions:
        print(version)


def set_default_version(version: str):
    version_folder = set_global_python(version)
    print(f"pvm: global python set to {version_folder}")

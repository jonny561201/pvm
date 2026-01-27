from svc.constants.file_constants import File, Architecture, OS
from svc.utilities.folder_utils import get_python_version_folders, set_global_python, create_version_directory
from svc.utilities.install_utils import extract_zip, download_python_release, delete_tar_file
from svc.utilities.prebuilt_release_utils import get_python_release_tag, get_python_releases, filter_python_release


def get_latest_release_version(version: str):
    print('...identifying latest release...')
    tag = get_python_release_tag()
    print('...getting python releases...')
    releases = get_python_releases(tag)
    # TODO: filter should take in version
    release = filter_python_release(releases, OS.APPLE, Architecture.INTEL)
    print('...downloading python version...')
    file_name = f"{version}.tgz"
    folder_name = create_version_directory(release[0])
    directory = File.VERSION_DIR / folder_name
    download_python_release(release[0], directory, file_name)
    print('...extracting python version...')
    extract_zip(directory, file_name)
    delete_tar_file(directory, file_name)



def get_python_versions():
    directories = get_python_version_folders(File.VERSION_DIR)
    versions = sorted([directory.name for directory in directories])
    for version in versions:
        print(version)


def set_default_version(version: str):
    set_global_python(version)
    print(f"pvm: global python set to {version}")

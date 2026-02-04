from svc.constants.file_constants import File


def set_global_version_file(version: str):
    version_file = File.CURRENT_DIR / "global-version"
    with open(version_file, 'w') as f:
        f.write(version)
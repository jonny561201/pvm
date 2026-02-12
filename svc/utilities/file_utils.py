import os
import sys
from pathlib import Path

from svc.constants.file_constants import File, OS
from svc.utilities.folder_utils import get_python_version_folders


def set_global_version_file(version: str):
    version_file = File.CURRENT_DIR / "global-version"
    with open(version_file, 'w') as f:
        f.write(version)


#TODO: prioritize the PVM_VERSION env var!
def get_global_version() -> str:
    version_file = File.CURRENT_DIR / "global-version"
    if not version_file.is_file():
        return '--- Not found ---'

    with open(version_file, 'r') as f:
        return f.read().strip()


def set_global_python(version: str) -> str:
    folders = get_python_version_folders()
    folder = next((folder for folder in folders if version in folder.name) , None)
    if not folder:
        sys.exit(f"python {version} is not installed")

    target = _get_python_executable(folder.name)
    tmp_link = File.CURRENT_PYTHON.with_suffix(".tmp")

    if tmp_link.exists() or tmp_link.is_symlink():
        tmp_link.unlink()

    os.symlink(target, tmp_link)
    os.replace(tmp_link, File.CURRENT_PYTHON)

    return folder.name


def _get_python_executable(folder: str) -> Path:
    python = File.VERSION_DIR / folder / 'python' / 'python.exe' if OS.detect() == OS.WINDOWS else File.VERSION_DIR / folder / 'python' / 'bin' / 'python'

    if not python.is_file() or python is None:
        sys.exit(f"Unable to locate python executable in {folder}")
    return python


# import ctypes
# import sys
# import os
#
# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False
#
# def relaunch_as_admin():
#     params = " ".join([f'"{arg}"' for arg in sys.argv])
#     ctypes.windll.shell32.ShellExecuteW(
#         None,
#         "runas",
#         sys.executable,
#         params,
#         None,
#         1,
#     )
#     sys.exit()
#
# if __name__ == "__main__":
#     if os.name == "nt" and not is_admin():
#         relaunch_as_admin()
#
#     # Now we are elevated
#     os.symlink("target", "link_name")
import sys
from pathlib import Path


class FileMode:
    READ_WRITE_EXEC = 0o700
    READ = 0o500
    WRITE = 0o400
    EXEC = 0o400


class File:
    PVM_DIR = Path.home() / '.pvm'
    VERSION_DIR = PVM_DIR / 'versions'
    CURRENT_DIR = PVM_DIR / 'bin'
    CURRENT_PYTHON = CURRENT_DIR / 'python'


class OS:
    APPLE = 'apple-darwin'
    WINDOWS = 'windows'
    LINUX = 'linux'
    _mapping = {'linux': LINUX, 'windows': WINDOWS, 'darwin': APPLE, 'win32': WINDOWS}

    @staticmethod
    def get_os_name():
        system = sys.platform
        return OS._mapping.get(system, system.lower())


class Architecture:
    ARM = 'aarch64'
    INTEL = 'x86_64'

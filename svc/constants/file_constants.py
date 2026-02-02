import platform
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
    _mapping = {'linux': LINUX, 'windows': WINDOWS, 'darwin': APPLE, 'win32': WINDOWS, 'msys': WINDOWS, 'cygwin': WINDOWS}

    @staticmethod
    def get_os():
        system = sys.platform.lower()
        return OS._mapping.get(system, system)


class Architecture:
    ARM = 'aarch64'
    INTEL = 'x86_64'
    _mapping = {'arm64': ARM, 'aarch64': ARM, 'armv7l': ARM, 'armv6l': ARM, 'x86_64': INTEL, 'AMD64': INTEL, 'i386': INTEL, 'i686': INTEL}

    @staticmethod
    def get_arch():
        machine = platform.machine().lower()
        return Architecture._mapping.get(machine, machine)

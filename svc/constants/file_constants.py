from pathlib import Path


class FileMode:
    READ_WRITE_EXEC = 0o700


class File:
    PVM_DIR = Path.home() / '.pvm'
    VERSION_DIR = PVM_DIR / 'versions'
    CURRENT_DIR = PVM_DIR / 'bin'
    CURRENT_PYTHON = CURRENT_DIR / 'python'


class OS:
    APPLE = 'apple-darwin'
    WINDOWS = 'windows'


class Architecture:
    ARM = 'aarch64'
    INTEL = 'x86_64'

from pathlib import Path


class FileMode:
    READ_WRITE_EXEC = 0o700


class File:
    PVM_DIR = Path.home() / '.pvm'
    VERSION_DIR = Path.home() / '.pvm' / 'versions'
    CURRENT_DIR = Path.home() / '.pvm' / 'current'
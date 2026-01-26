from pathlib import Path


class FileMode:
    read_write_exec = 0o700


class File:
    pvm_dir = Path.home() / ".pvm"
import hashlib
import os
from enum import Enum

from hckr.utils.MessageUtils import colored, info, checkOnlyOnePassed, error, success


class HashType(str, Enum):
    MD5 = ("md5",)
    SHA1 = ("sha1",)
    SHA256 = ("sha256",)
    SHA512 = ("sha512",)


def human_readable_size(size, decimal_places=2):
    # Define the threshold of bytes for units
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def checkFile(_file, _chunk_size):
    if os.path.isdir(_file):
        raise Exception(f"Path is directory, please pass file path: '{_file}'")
    if not os.path.exists(_file):
        raise Exception(f"File not found, Please verify file path: '{_file}'")
    stat_info = os.stat(_file)
    info(
        f"File size: {colored(human_readable_size(stat_info.st_size), 'yellow')}, Using chunk size: {colored(human_readable_size(_chunk_size), 'yellow')}"
    )


def hashStringOrFile(_str, _file, _method, _chunk_size):
    checkOnlyOnePassed("str", _str, "file", _file)
    digest = None
    try:
        m = hashlib.new(_method)
        if _str:
            info(f"Finding hash for string: {_str}")
            m.update(_str.encode())
            digest = m.hexdigest()
        elif _file:
            checkFile(_file, _chunk_size)
            info(f"Finding hash for file: {colored(_file, 'yellow')}")
            with open(_file, "rb") as f:
                # Read and update hash in chunks to avoid using too much memory
                for chunk in iter(lambda: f.read(_chunk_size), b""):
                    m.update(chunk)
                digest = m.hexdigest()
        else:
            error("Invalid option")
    except Exception as e:
        error(f"Some error occurred\n {e}")
    if digest:
        success(f"{_method.upper()}: {digest}")

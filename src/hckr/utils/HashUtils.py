from enum import StrEnum
import hashlib

from hckr.utils.MessageUtils import *


class HashType(StrEnum):
    MD5 = ("md5",)
    SHA1 = ("sha1",)
    SHA256 = ("sha256",)
    SHA512 = ("sha512",)


def hashStringOrFile(_str, _file, _method, _chunk_size):
    checkOnlyOnePassed("str", _str, "file", _file)
    try:
        m = hashlib.new(_method)
        if _str:
            info(f"Finding hash for string: {_str}")
            m.update(_str.encode())
            return m.hexdigest()
        if _file:
            info(f"Finding hash for file: {colored(_file, 'blue')}")
            info(f"Using default chunk size: {colored(_chunk_size, 'blue')} bytes")
            with open(_file, "rb") as f:
                # Read and update hash in chunks to avoid using too much memory
                for chunk in iter(lambda: f.read(_chunk_size), b""):
                    m.update(chunk)
                return m.hexdigest()
    except Exception as e:
        error(f"Some error occurred\n {e}")

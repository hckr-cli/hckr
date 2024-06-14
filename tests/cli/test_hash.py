from pathlib import Path
from typing import Any

from click.testing import CliRunner
from hckr.cli.hash import sha1, sha256, sha512, md5
from hckr.utils.HashUtils import HashType

current_directory = Path(__file__).parent
HASH_STRING = "Nobody inspects the spammish repetition\n"
HASH_FILE = current_directory / "resources" / "hash" / "test.txt"
EXPECTED_HASHES = {
    "md5": "532027503f1149e968f8465a1b15b62f",
    "sha1": "55cd84c899a3d9f41d5a4d1be4ac57b37551db00",
    "sha256": "a429ddcbe4d2ba357a8c72827f1c9beb878c42081df360c197678263915f3372",
    "sha512": "de60537b3bde7838b3e6763cc94180f0525d17c0335fc2a513eb067c9db367f712a045fa35a6b19c2c4ffd2b81c3091944d94131908daef8a8b8e8c475a56792",
}


def _get_hash_command(method) -> Any:
    if method == HashType.SHA1:
        return sha1
    elif method == HashType.SHA256:
        return sha256
    elif method == HashType.MD5:
        return md5
    elif method == HashType.SHA512:
        return sha512
    else:
        raise Exception(f"Invalid Hash method {method}")


# POSITIVE CASES
def test_string_hashes():
    runner = CliRunner()
    for hash_type in EXPECTED_HASHES:
        print(f"\n{'-' * 50}\n")
        result = runner.invoke(_get_hash_command(hash_type), ["--string", HASH_STRING])
        print(result.output)
        assert result.exit_code == 0
        assert EXPECTED_HASHES[hash_type] in result.output.replace("\n", "")


def test_file_hashes():
    runner = CliRunner()
    for hash_type in EXPECTED_HASHES:
        print(f"\n{'-' * 50}\n")
        result = runner.invoke(_get_hash_command(hash_type), ["--file", HASH_FILE])
        print(result.output)
        assert result.exit_code == 0
        assert "Using chunk size: 4.00 KB" in result.output
        assert EXPECTED_HASHES[hash_type] in result.output.replace("\n", "")


def test_file_hash_with_chunk_size():
    runner = CliRunner()
    # check for all the types
    for hash_type in EXPECTED_HASHES:
        print(f"\n{'-' * 50}\n")
        result = runner.invoke(
            _get_hash_command(hash_type), ["--file", HASH_FILE, "--chunk-size", 1024]
        )
        print(f"{hash_type}: {result.output}")
        assert result.exit_code == 0
        assert "Using chunk size: 1.00 KB" in result.output
        assert EXPECTED_HASHES[hash_type] in result.output.replace("\n", "")


def test_file_hash_invalid_path():
    runner = CliRunner()
    # check for all the types
    for hash_type in EXPECTED_HASHES:
        print(f"\n{'-' * 50}\n")
        result = runner.invoke(
            _get_hash_command(hash_type), ["--file", "/invalid/path/file"]
        )
        print(f"{hash_type}: {result.output}")
        assert result.exit_code == 0
        assert (
            "Some error occurred File not found, Please verify file path"
            in result.output.replace("\n", "")
        )


def test_file_hash_is_dir():
    runner = CliRunner()
    # check for all the types
    for hash_type in EXPECTED_HASHES:
        print(f"\n{'-' * 50}\n")
        result = runner.invoke(
            _get_hash_command(hash_type), ["--file", current_directory]
        )
        print(f"{hash_type}: {result.output}")
        assert result.exit_code == 0
        assert "Path is directory, please pass file path" in result.output.replace(
            "\n", ""
        )

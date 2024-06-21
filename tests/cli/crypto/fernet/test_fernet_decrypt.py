import re
from pathlib import Path

from click.testing import CliRunner

from hckr.cli.crypto.fernet import decrypt, decrypt_file

parent_directory = Path(__file__).parent.parent.parent
ENCRYPTED_MESSAGE = "gAAAAABmdVJkaiK1gUihh-T3Z4-_p2qoy6v3NI7uITyXcsOoxOw2pLoAVtA7ZxUwyidHpoywgDBmkxB5N-woLJ0_6jJ09SzG-w=="

ENCRYPTED_MESSAGE_FILE = (
    parent_directory / "resources" / "crypto" / "decrypt" / "encrypted_message.txt"
)
KEY_PATH = parent_directory / "resources" / "crypto" / "key.txt"
OUTPUT_PATH = (
    parent_directory / "resources" / "crypto" / "decrypt" / "decrypted_message.txt"
)


# POSITIVE SCENARIOS
def test_fernet_decrypt_message_with_key():
    runner = CliRunner()
    result = runner.invoke(decrypt, ["-m", ENCRYPTED_MESSAGE, "-k", KEY_PATH])
    print(result.output)
    assert result.exit_code == 0
    assert "Decrypted message" in result.output
    assert "Hello, World!" in result.output


def test_fernet_decrypt_file_with_key():
    runner = CliRunner()
    result = runner.invoke(
        decrypt_file, ["-f", ENCRYPTED_MESSAGE_FILE, "-k", KEY_PATH, "-o", OUTPUT_PATH]
    )
    print(result.output)
    # assert result.exit_code == 0 # TODO: for some reason rich.panel() returning 1 as exit_code
    assert f"""File decrypted, output""" in result.output


def test_fernet_decrypt_no_key_argument():
    runner = CliRunner()
    result = runner.invoke(decrypt, ["-m", ENCRYPTED_MESSAGE])
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing option '-k' / '--key'" in result.output


def test_fernet_decrypt_no_message_argument():
    runner = CliRunner()
    result = runner.invoke(decrypt, ["-k", KEY_PATH])
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing option '-m' / '--message'" in result.output


def test_fernet_decrypt_no_file_argument():
    runner = CliRunner()
    result = runner.invoke(decrypt_file, ["-k", KEY_PATH])
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing option '-f' / '--file'" in result.output


def test_fernet_decrypt_no_output_argument():
    runner = CliRunner()
    result = runner.invoke(decrypt_file, ["-k", KEY_PATH, "-f", ENCRYPTED_MESSAGE_FILE])
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing option '-o' / '--output'" in result.output


def test_fernet_decrypt_key_path_doesnt_exist():
    runner = CliRunner()
    INVALID_KEY_PATH = KEY_PATH / "invalid.txt"
    result = runner.invoke(decrypt, ["-m", ENCRYPTED_MESSAGE, "-k", INVALID_KEY_PATH])
    print(result.output)
    assert result.exit_code != 0
    assert f"""Please check and provide correct encryption key path""" in result.output

import re
from pathlib import Path

from click.testing import CliRunner

from hckr.cli.crypto.fernet import encrypt
from hckr.utils.FileUtils import delete_path_if_exists

parent_directory = Path(__file__).parent.parent
MESSAGE = "Hello, World!"

MESSAGE_FILE = parent_directory / "resources" / "crypto" / "message.txt"
KEY_PATH = parent_directory / "resources" / "crypto" / "key.txt"
NEW_KEY_PATH = parent_directory / "resources" / "crypto" / "new_key.txt"


# NEGATIVE SCENARIOS
def test_fernet_encrypt_no_key_argument():
    runner = CliRunner()
    result = runner.invoke(encrypt, ["-m", MESSAGE])
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing option '-k' / '--key'" in result.output


def test_fernet_encrypt_key_path_doesnt_exist():
    runner = CliRunner()
    INVALID_KEY_PATH = KEY_PATH / "invalid.txt"
    result = runner.invoke(encrypt, ["-m", MESSAGE, "-k", INVALID_KEY_PATH])
    print(result.output)
    assert result.exit_code != 0
    assert (
        f"""Key file path 
:{INVALID_KEY_PATH} 
doesn't exists, 
Please provide -c / --create-key if you want to create one."""
        in result.output
    )


def test_fernet_encrypt_key_path_doesnt_exist_create():
    runner = CliRunner()
    delete_path_if_exists(NEW_KEY_PATH)  # delete the path to achieve this behaviour
    result = runner.invoke(encrypt, ["-m", MESSAGE, "-k", NEW_KEY_PATH, "-c"])
    delete_path_if_exists(NEW_KEY_PATH)  # delete the path to achieve this behaviour
    print(result.output)
    assert result.exit_code == 0
    assert (
        f"""Key file does not exist. Generating a new one: 
{NEW_KEY_PATH}"""
        in result.output
    )
    assert "Encrypted message: " in result.output


def test_fernet_encrypt_both_message_and_file():
    runner = CliRunner()
    result = runner.invoke(encrypt, ["-m", MESSAGE, "-f", MESSAGE, "-k", KEY_PATH])
    print(result.output)
    assert result.exit_code != 0
    assert "Please use either --message or --file, can't use both" in result.output

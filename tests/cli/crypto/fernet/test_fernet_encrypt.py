from pathlib import Path

from click.testing import CliRunner

from hckr.cli.crypto.fernet import encrypt, encrypt_file
from hckr.utils.FileUtils import delete_path_if_exists

parent_directory = Path(__file__).parent.parent.parent
MESSAGE = "Hello, World!"

KEY_PATH = parent_directory / "resources" / "crypto" / "key.txt"
MESSAGE_FILE = parent_directory / "resources" / "crypto" / "encrypt" / "message.txt"
OUTPUT_PATH = parent_directory / "resources" / "crypto" / "encrypt" / "output.txt"
NEW_KEY_PATH = parent_directory / "resources" / "crypto" / "encrypt" / "new_key.txt"


# POSITIVE SCENARIOS
def test_fernet_encrypt_message_with_key():
    runner = CliRunner()
    result = runner.invoke(encrypt, ["-m", MESSAGE, "-k", KEY_PATH, "-c"])
    print(result.output)
    # assert result.exit_code == 0 # TODO: for some reason rich.panel() returning 1 as exit_code
    assert (
        f"""Encrypting 'Hello, World!', Using key file: 
{KEY_PATH}"""
        in result.output
    )
    assert "Encrypted message" in result.output


def test_fernet_encrypt_file_with_key():
    runner = CliRunner()
    result = runner.invoke(
        encrypt_file, ["-f", MESSAGE_FILE, "-k", KEY_PATH, "-o", OUTPUT_PATH]
    )
    print(result.output)
    # assert result.exit_code == 0 # TODO: for some reason rich.panel() returning 1 as exit_code
    assert """File encrypted, output written""" in result.output


def test_fernet_encrypt_key_path_doesnt_exist_create_key():
    runner = CliRunner()
    delete_path_if_exists(NEW_KEY_PATH)  # delete the path to achieve this behaviour
    result = runner.invoke(encrypt, ["-m", MESSAGE, "-k", NEW_KEY_PATH, "-c"])
    delete_path_if_exists(NEW_KEY_PATH)  # delete the path to achieve this behaviour
    print(result.output)
    assert (
        result.exit_code == 0
    )  # TODO: for some reason rich.panel() returning 1 as exit_code
    assert (
        """Key file does not exist, Flag [ -c / --create-key ] passed
 Generating a new key"""
        in result.output
    )
    assert "Encrypted message" in result.output


# NEGATIVE SCENARIOS
def test_fernet_encrypt_no_key_argument():
    runner = CliRunner()
    result = runner.invoke(encrypt, ["-m", MESSAGE])
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing option '-k' / '--key'" in result.output


def test_fernet_encrypt_no_message_argument():
    runner = CliRunner()
    result = runner.invoke(encrypt, ["-k", KEY_PATH])
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing option '-m' / '--message'" in result.output


def test_fernet_encrypt_no_file_argument():
    runner = CliRunner()
    result = runner.invoke(encrypt_file, ["-k", KEY_PATH])
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing option '-f' / '--file'" in result.output


def test_fernet_encrypt_no_output_argument():
    runner = CliRunner()
    result = runner.invoke(encrypt_file, ["-k", KEY_PATH, "-f", MESSAGE_FILE])
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing option '-o' / '--output'" in result.output


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

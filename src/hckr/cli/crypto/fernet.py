import logging
from pathlib import Path

import click

from hckr.utils.CryptoUtils import (
    encrypt_message,
    checkAndCreateKey,
    encrypt_file_content,
    decrypt_message,
    decrypt_file_content,
)
from hckr.utils.FileUtils import load_file, save_file
from hckr.utils.MessageUtils import (
    success,
    error,
    colored,
    info,
)
from ..crypto import crypto
import rich
from rich.panel import Panel


@crypto.group(
    help="cryptography using fernet",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def fernet():
    pass


@fernet.command()
@click.option(
    "-k",
    "--key",
    type=click.Path(),
    help="Path to the encryption key file.",
    required=True,
)
@click.option("-m", "--message", help="message to be encrypted", required=True)
@click.option(
    "-c",
    "--create-key",
    help="Flat to auto create key if key path doesn't exists",
    default=False,
    is_flag=True,
    required=False,
)
def encrypt(key, message, create_key):
    """
    This command encrypts a TEXT message using **Fernet** key.

    **Example Usage**:

    * Encrypt a message with given key file

    .. code-block:: shell

        $ hckr crypto fernet encrypt -m 'hello'  -k 'key.txt'

    * Encrypt a message and create new key file

    .. code-block:: shell

        $ hckr crypto fernet encrypt -m 'hello'  -k 'key.txt' -c

    **Command Reference**:
    """

    checkAndCreateKey(key, message, create_key)
    new_key = load_file(key)
    encrypted_message = encrypt_message(message, new_key)
    rich.print(
        Panel(
            encrypted_message.decode(),
            expand=True,
            title="Encrypted message",
        )
    )


@fernet.command()
@click.option(
    "-k",
    "--key",
    type=click.Path(),
    help="Path to the encryption key file.",
    required=True,
)
@click.option(
    "-f", "--file", type=click.Path(), help="File to be encrypted", required=True
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="Output file containing encrypted file",
    required=True,
)
@click.option(
    "-c",
    "--create-key",
    help="Flat to auto create key if key path doesn't exists",
    default=False,
    is_flag=True,
    required=False,
)
def encrypt_file(key, file, output, create_key):
    """
    This command encrypts a file PATH using **Fernet** key and generates output file

    **Example Usage**:

    * Encrypt a file with given key file

    .. code-block:: shell

        $ hckr crypto fernet encrypt -f 'message.txt'  -k 'key.txt' -o 'output.txt'

    * Encrypt a file and create new key file

    .. code-block:: shell

        $ hckr crypto fernet encrypt -f 'message.txt'  -k 'key.txt' -o 'output.txt' -c

    **Command Reference**:
    """
    checkAndCreateKey(key, file, create_key)
    new_key = load_file(key)
    encrypted_content = encrypt_file_content(file, new_key)
    save_file(encrypted_content, output)
    success(f"File encrypted, output written")
    rich.print(
        Panel(
            output,
            expand=True,
            title="File Output",
        )
    )


@fernet.command()
@click.option(
    "-k",
    "--key",
    type=click.Path(),
    help="Path to the encryption key file.",
    required=True,
)
@click.option("-m", "--message", help="Message to be decrypted", required=True)
def decrypt(key, message):
    """
    This command decrypts a TEXT message using **Fernet** key.

    **Example Usage**:

    * Decrypt a message with given key file

    .. code-block:: shell

        $ hckr crypto fernet decrypt -m 'gAAAAABmdVJkaiK1gUihh-T3Z4-_p2qoy6v3NI7uITyXcsOow==' -k 'key.txt'

    **Command Reference**:
    """
    info(
        f"Decrypting '{colored(message, 'magenta')}', Using key file: {colored(key, 'yellow')}"
    )
    if not Path(key).exists():
        error(
            f"Key file path :{key} doesn't exists, \nPlease check and provide correct encryption key path."
        )
        exit(1)

    new_key = load_file(key)
    decrypted_message = decrypt_message(message, new_key)
    rich.print(
        Panel(
            decrypted_message,
            expand=True,
            title="Decrypted message",
        )
    )


@fernet.command()
@click.option(
    "-k",
    "--key",
    type=click.Path(),
    help="Path to the encryption key file.",
    required=True,
)
@click.option(
    "-f", "--file", type=click.Path(), help="File to be decrypted", required=True
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="Output file containing decrypted file",
    required=True,
)
def decrypt_file(key, file, output):
    """
    This command decrypts a file PATH using **Fernet** key and generates output file

    **Example Usage**:

    * Encrypt a file with given key file

    .. code-block:: shell

        $ hckr crypto fernet decrypt -f 'encrypted_message.txt'  -k 'key.txt' -o 'output.txt'


    **Command Reference**:
    """
    info(
        f"Decrypting '{colored(file, 'magenta')}', Using key file: {colored(key, 'yellow')}"
    )
    if not Path(key).exists():
        error(
            f"Key file path :{key} doesn't exists, \nPlease check and provide correct encryption key path."
        )
        exit(1)

    new_key = load_file(key)
    decrypted_content = decrypt_file_content(file, new_key)
    save_file(decrypted_content, output)
    success(f"File decrypted, output written")
    logging.debug(f"Message head:\n'{decrypted_content.decode()[:100]}'")
    rich.print(
        Panel(
            output,
            expand=True,
            title="File Output",
        )
    )

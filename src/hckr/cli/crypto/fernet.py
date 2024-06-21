from pathlib import Path

import click

from hckr.utils.CryptoUtils import (
    generate_key,
    encrypt_message,
    decrypt_message,
)
from hckr.utils.FileUtils import save_file, load_file
from hckr.utils.MessageUtils import (
    warning,
    info,
    colored,
    success,
    error,
    checkOnlyOnePassed,
)
from ..crypto import crypto


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
@click.option("-m", "--message", help="message to be encrypted", required=False)
@click.option(
    "-f", "--file", type=click.Path(), help="File to be hashed", required=False
)
@click.option(
    "-c",
    "--create-key",
    help="Flat to auto create key if key path doesn't exists",
    default=False,
    is_flag=True,
    required=False,
)
def encrypt(key, message, file, create_key):
    checkOnlyOnePassed("message", message, "file", file)
    if not Path(key).exists():
        if create_key:
            warning(
                f"Key file does not exist. Generating a new one: {colored(key, 'magenta')}"
            )
            new_key = generate_key()
            save_file(new_key, key)
        else:
            error(
                f"Key file path :{key} doesn't exists, \nPlease provide -c / --create-key if you want to create one."
            )
            exit(1)
    else:
        info(
            f"Encrypting '{colored(message, 'magenta')}', Using key file: {colored(key, 'yellow')}"
        )
        new_key = load_file(key)
    encrypted_message = encrypt_message(message, new_key)
    success(f"Encrypted message: {encrypted_message}")


# @fernet.command()
# @click.argument("encrypted_message")
# @click.option(
#     "--key", type=click.Path(), help="Path to the encryption key file.", required=True
# )
# def decrypt(encrypted_message, key):
#     if not Path(key).exists():
#         error(f"Key file not found: {key}, please provide a valid key path")
#         exit(1)
#     try:
#         loaded_key = load_file(key)
#         decrypted_message = decrypt_message(encrypted_message.encode(), loaded_key)
#         success(f"Decrypted message: {colored(decrypted_message, 'magenta')}")
#     except Exception as e:
#         error(
#             f"Error decrypting message with given key {key}, Please validate key \n {e}"
#         )

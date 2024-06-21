import click

from hckr.utils.CryptoUtils import (
    encrypt_message,
    checkAndCreateKey,
    encrypt_file_content,
)
from hckr.utils.FileUtils import load_file
from hckr.utils.MessageUtils import (
    success,
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
    "-c",
    "--create-key",
    help="Flat to auto create key if key path doesn't exists",
    default=False,
    is_flag=True,
    required=False,
)
def encrypt(key, message, create_key):
    checkAndCreateKey(key, message, create_key)
    new_key = load_file(key)
    encrypted_message = encrypt_message(message, new_key)
    success(f"Encrypted message: {encrypted_message}")


@fernet.command()
@click.option(
    "-k",
    "--key",
    type=click.Path(),
    help="Path to the encryption key file.",
    required=True,
)
@click.option(
    "-f", "--file", type=click.Path(), help="File to be encrypted", required=False
)
@click.option(
    "-c",
    "--create-key",
    help="Flat to auto create key if key path doesn't exists",
    default=False,
    is_flag=True,
    required=False,
)
def encrypt_file(key, file, create_key):
    checkAndCreateKey(key, file, create_key)
    new_key = load_file(key)
    encrypted_message = encrypt_file_content(file, new_key)
    success(f"Encrypted file output: {encrypted_message}")


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

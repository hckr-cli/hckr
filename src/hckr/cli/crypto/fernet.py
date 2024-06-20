from pathlib import Path

import click

from hckr.utils.CryptoUtils import (
    generate_key,
    save_file,
    load_file,
    encrypt_message,
    decrypt_message,
)
from hckr.utils.MessageUtils import warning, info, colored, success, error
from ..crypto import crypto


@crypto.group(
    help="cryptography using fernet",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def fernet():
    pass


@fernet.command()
@click.argument("message")
@click.option(
    "--key", type=click.Path(), help="Path to the encryption key file.", required=True
)
def encrypt(message, key):
    if not Path(key).exists():
        warning(
            f"Key file does not exist. Generating a new one in current path {colored(key, 'magenta')}"
        )
        new_key = generate_key()
        save_file(new_key, key)
    else:
        info(
            f"Encrypting '{colored(message, 'magenta')}', Using key file: {colored(key, 'yellow')}"
        )
        new_key = load_file(key)
    encrypted_message = encrypt_message(message, new_key)
    success(f"Encrypted message: {encrypted_message}")


@fernet.command()
@click.argument("encrypted_message")
@click.option(
    "--key", type=click.Path(), help="Path to the encryption key file.", required=True
)
def decrypt(encrypted_message, key):
    if not Path(key).exists():
        error(f"Key file not found: {key}, please provide a valid key path")
        exit(1)
    try:
        loaded_key = load_file(key)
        decrypted_message = decrypt_message(encrypted_message.encode(), loaded_key)
        success(f"Decrypted message: {colored(decrypted_message, 'magenta')}")
    except Exception as e:
        error(
            f"Error decrypting message with given key {key}, Please validate key \n {e}"
        )

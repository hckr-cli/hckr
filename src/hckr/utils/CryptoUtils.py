from pathlib import Path

from cryptography.fernet import Fernet

from hckr.utils.MessageUtils import warning, colored, error, info
from .FileUtils import save_file, load_file


# Generate a key and instantiate a Fernet instance
def generate_key():
    return Fernet.generate_key()


# Encrypt a message
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message


# Encrypt a message
def encrypt_file_content(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        original = file.read()
    encrypted = f.encrypt(original)
    return encrypted


# Decrypt a message
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message


def decrypt_file_content(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        original = file.read()
    decrypted_message = f.decrypt(original)
    return decrypted_message


def checkAndCreateKey(key, content, create_key):
    if not Path(key).exists():
        if create_key:
            warning(
                f"Key file does not exist, Flag [ -c / --create-key ] passed\n Generating a new key: {colored(key, 'magenta')}"
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
            f"Encrypting '{colored(content, 'magenta')}', Using key file: {colored(key, 'yellow')}"
        )

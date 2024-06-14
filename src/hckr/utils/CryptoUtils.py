from cryptography.fernet import Fernet


# Generate a key and instantiate a Fernet instance
def generate_key():
    return Fernet.generate_key()


# Save the key to a file
def save_key(key, file_path):
    with open(file_path, "wb") as key_file:
        key_file.write(key)


# Load the key from a file
def load_key(file_path):
    with open(file_path, "rb") as key_file:
        key = key_file.read()
    return key


# Encrypt a message
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message


# Decrypt a message
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

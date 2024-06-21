from cryptography.fernet import Fernet


# Generate a key and instantiate a Fernet instance
def generate_key():
    return Fernet.generate_key()


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

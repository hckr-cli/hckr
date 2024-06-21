import logging
from pathlib import Path


# Save the key to a file
def save_file(key, file_path):
    with open(file_path, "wb") as key_file:
        key_file.write(key)


# Load the key from a file
def load_file(file_path):
    with open(file_path, "rb") as key_file:
        key = key_file.read()
    return key


def delete_path_if_exists(path):
    """Delete a file or directory if it exists using pathlib."""
    path = Path(path)
    if path.exists():
        if path.is_file():
            logging.info("path is a file, deleted.")
            path.unlink()  # Remove the file
        elif path.is_dir():
            logging.info("path is a directory, removing recursively.")
            path.rmdir()  # Remove the directory, note this directory must be empty
        print(f"Deleted: {path}")
    else:
        print(f"No such path: {path}")

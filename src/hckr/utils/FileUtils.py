import logging
from pathlib import Path

from hckr.utils.MessageUtils import error


# Save the key to a file
def save_file(content, file_path):
    try:
        path = Path(file_path)
        # creating any intermediate directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as key_file:
            key_file.write(content)
    except Exception as e:
        logging.debug(e)
        error(f"Some error occurred while saving {file_path}\n{e}")
        exit(1)


# Load the key from a file
def load_file(file_path):
    checkFileExists(file_path)
    try:
        with open(file_path, "rb") as key_file:
            content = key_file.read()
        return content
    except Exception as e:
        logging.debug(e)
        error(f"Some error occurred while reading {file_path}\n{e}")
        exit(1)


def checkFileExists(file_path):
    logging.debug(f"checkFileExists() invoked with {file_path}")
    path = Path(file_path)
    if path.exists():
        if path.is_file():
            logging.debug("path is a file")
        elif path.is_dir():
            logging.info("path is a directory")
            error(f"Path {path} is a directory")
            exit(1)
    else:
        error(f"File not found, please verify path: {path}")
        exit(1)


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

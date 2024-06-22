import logging
import os
from pathlib import Path

from hckr.utils.MessageUtils import error, info, colored, warning

from enum import Enum


class FileFormat(str, Enum):
    CSV = "csv"
    AVRO = "avro"
    JSON = "json"
    EXCEL = "excel"
    PARQUET = "parquet"
    INVALID = "invalid"

    @staticmethod
    def fileExtToFormat(file_path, file_extension):
        file_type_extension_map = {
            # ".txt": FileFormat.CSV,
            # ".text": FileFormat.CSV,
            ".csv": FileFormat.CSV,
            ".json": FileFormat.JSON,
            ".xlsx": FileFormat.EXCEL,
            ".xls": FileFormat.EXCEL,
            ".parquet": FileFormat.PARQUET,
            ".avro": FileFormat.AVRO,
        }

        _format = file_type_extension_map.get(
            file_extension.lower(), FileFormat.INVALID
        )
        if _format == FileFormat.INVALID:
            warning("Unable to infer file format from file")
            error(
                f"Invalid file extension {colored(file_extension, 'yellow')} for file {colored(file_path, 'magenta')}, "
                f"\nAvailable extensions {sorted(file_type_extension_map.keys())}\nOr Please provide format using -f / --format option"
            )
            exit(1)
        return _format

    @staticmethod
    def validFormats():
        return [str(x) for x in FileFormat if str(x) != str(FileFormat.INVALID)]

    def __str__(self):
        return self.value


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


# validate if file extension is one of given
def validate_file_extension(file_path, expected_extensions):
    # Extract the extension from the file path
    _, file_extension = os.path.splitext(file_path)
    # Check if the extension is in the list of expected extensions
    if file_extension.lower() not in expected_extensions:
        error(
            f"Invalid file extension: {file_extension} in file: {file_path}\n allowed: {expected_extensions}"
        )
        exit(1)


# validate if file extension is one of given
def get_file_format_from_extension(file_path):
    if not file_path:
        return FileFormat.INVALID
    # Extract the extension from the file path
    # path = Path(file_path)
    _, file_extension = os.path.splitext(file_path)
    logging.info(f"file extension from file {file_path} is {file_extension}")
    return FileFormat.fileExtToFormat(file_path, file_extension)

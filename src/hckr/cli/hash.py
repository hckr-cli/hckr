import click
from cron_descriptor import get_description  # type: ignore
from hckr.utils.HashUtils import hashStringOrFile, HashType


@click.group(
    help="hash commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def hash():
    pass


@click.option("-s", "--string", help="String to be hashed", required=False)
@click.option(
    "-f", "--file", type=click.Path(), help="File to be hashed", required=False
)
@click.option(
    "-c",
    "--chunk-size",
    help="Size of chunks for file hash",
    required=False,
    default=4096,
)
@hash.command(help="hash using MD5 algorithm")
def md5(string, file, chunk_size):
    hashStringOrFile(string, file, HashType.MD5, chunk_size)


@click.option("-s", "--string", help="String to be hashed", required=False)
@click.option(
    "-f", "--file", type=click.Path(), help="File to be hashed", required=False
)
@click.option(
    "-c",
    "--chunk-size",
    help="Size of chunks for file hash",
    required=False,
    default=4096,
)
@hash.command(help="hash using SHA1 algorithm")
def sha1(string, file, chunk_size):
    hashStringOrFile(string, file, HashType.SHA1, chunk_size)


@click.option("-s", "--string", help="String to be hashed", required=False)
@click.option(
    "-f", "--file", type=click.Path(), help="File to be hashed", required=False
)
@click.option(
    "-c",
    "--chunk-size",
    help="Size of chunks for file hash",
    required=False,
    default=4096,
)
@hash.command(help="hash using SHA256 algorithm")
def sha256(string, file, chunk_size):
    hashStringOrFile(string, file, HashType.SHA256, chunk_size)


@click.option("-s", "--string", help="String to be hashed", required=False)
@click.option(
    "-f", "--file", type=click.Path(), help="File to be hashed", required=False
)
@click.option(
    "-c",
    "--chunk-size",
    help="Size of chunks for file hash",
    required=False,
    default=4096,
)
@hash.command(help="hash using SHA512 algorithm")
def sha512(string, file, chunk_size):
    hashStringOrFile(string, file, HashType.SHA512, chunk_size)

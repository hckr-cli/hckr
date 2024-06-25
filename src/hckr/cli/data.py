import json
import logging

import click
import fastavro
import pandas as pd
import pyarrow as pa  # type: ignore
import rich
from cron_descriptor import get_description  # type: ignore
from faker import Faker
from pyarrow import parquet as pq  # type: ignore
from rich.panel import Panel

from hckr.utils.DataUtils import safe_faker_method, print_df_as_table, readFile
from hckr.utils.FileUtils import (
    validate_file_extension,
    get_file_format_from_extension,
    FileFormat,
)
from hckr.utils.MessageUtils import success, colored, info, error


@click.group(
    help="data related commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def data():
    pass


@data.command()
@click.option(
    "-c",
    "--count",
    default=10,
    help="Number of data entries to generate.",
    required=False,
)
@click.option(
    "-s",
    "--schema",
    type=click.Path(exists=True),
    help="Path to the JSON schema file.",
    required=True,
)
@click.option("-o", "--output", help="Output file path", required=True)
@click.option(
    "-f",
    "--format",
    help=f"Output file format, Options: {FileFormat.validFormats()} [default: Inferred from file extension]",
    required=False,
)
def faker(count, schema, output, format):
    """
    This command Generate fake Data in different file formats

    **Example Usage**:

    * let we have the following schema in format `{"column_name": "faker_provider"}`
    * Please find all faker provider  `here <https://faker.readthedocs.io/en/master/providers.html>`_

    .. code-block:: json
        :caption: schema.json

        {
            "user_name": "name",
            "user_address": "address",
            "user_email": "email"
        }

    * Generate **csv** data using schema

    .. code-block:: shell

        $ hckr data faker -s schema.json -o file.avro

    * Similarly, we can generate **avro** (or any other valid format) data

    .. code-block:: shell

        $ hckr data faker -s schema.json -o file.csv

    * We can also provide data format explicitly, if file extension is not clear

    .. code-block:: shell

        $ hckr data faker -s schema.json -o output -f csv


    **Command Reference**:
    """

    try:
        if not format:
            format = get_file_format_from_extension(output)
            info(
                f"File format is not passed, inferring from output file path {colored(output, 'yellow')}"
            )
            info(f"Format inferred: {colored(format, 'magenta')}")
        else:
            format = format.lower()
        fake = Faker()
        with open(schema, "r") as schema_file:
            schema = json.load(schema_file)

        records = []

        # Adjusted fake data generation
        for _ in range(count):
            entry = {
                key: safe_faker_method(fake, *value.split(":"))
                for key, value in schema.items()
            }
            records.append(entry)

        df = pd.DataFrame(records)

        if format == FileFormat.CSV:
            df.to_csv(output, index=False, quotechar='"', escapechar="\\")
        elif format == FileFormat.JSON:
            df.to_json(output, orient="records")
        elif format == FileFormat.EXCEL:
            validate_file_extension(output, [".xlsx", ".xls"])
            df.to_excel(output, index=False, engine="openpyxl")
        elif format == FileFormat.PARQUET:
            table = pa.Table.from_pandas(df)
            pq.write_table(table, output)
        elif format == FileFormat.AVRO:
            records = df.to_dict(orient="records")
            schema = {
                "doc": "Avro schema for generated data",
                "name": "Root",
                "type": "record",
                "fields": [
                    {"name": str(key), "type": ["null", "string"], "default": None}
                    for key in records[0]
                ],
            }
            parsed_schema = fastavro.parse_schema(schema)
            with open(output, "wb") as out:
                fastavro.writer(out, parsed_schema, records)
        else:
            error(
                f"Invalid file format {str(format)}, Available {FileFormat.validFormats()}"
            )
            exit(1)
        info(
            f"Generating {colored(count, 'magenta')} rows in {colored(format, 'yellow')} format."
        )
        # logging.debug(f"Data head:\n'{df.head()}'")

        print_df_as_table(df)
        success(
            f"Data written to {colored(output, 'magenta')} in {colored(format, 'yellow')} format."
        )

        rich.print(
            Panel(
                output,
                expand=True,
                title="File Output",
            )
        )
    except Exception as e:
        error(f"Some error occurred while generating data\n{e}")


@data.command()
@click.option("-i", "--input", help="Input file to peek into", required=True)
@click.option(
    "-c",
    "--count",
    default=10,
    help="Number of rows to show, [default: 10]",
    required=False,
)
@click.option(
    "-f",
    "--format",
    help="Output file format, if not provided it gets inferred from file extension",
    required=False,
)
def peek(input, count, format):
    """
    This command allows us to peek into top COUNT rows from a file

    **Example Usage**:

    * We can look into an input file by providing **-i** or **-\-input** option
    * It will show top 10 rows ( by default )

    .. code-block:: shell

        $ hckr data peek -i input.avro

    * We can also provide number of rows we want to see using **-c** or **-\-count** option

    .. code-block:: shell

        $ hckr data peek -i input.avro -c 20

    * We can also provide data format explicitly using **-f** or **-\-format** option, if file extension is not clear

    .. code-block:: shell

        $ hckr data peek -i input.data -f csv


    **Command Reference**:
    """
    try:
        info(
            f"Peeking {colored(count, 'magenta')} rows in file {colored(input, 'yellow')}"
        )
        if not format:
            format = get_file_format_from_extension(input)
            info(
                f"File format is not passed, inferring from file path {colored(input, 'yellow')}"
            )
            info(f"Format inferred: {colored(format, 'magenta')}")
        else:
            format = format.lower()

        # Adjusted fake data generation
        df = readFile(format, input)
        # logging.debug(f"Data head:\n'{df.head()}'")
        print_df_as_table(df, count=count)
    except Exception as e:
        error(
            f"Some error occurred while reading data {colored(input,'magenta')} in format {colored(format,'yellow')}\n{e}"
        )

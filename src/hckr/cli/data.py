import json
import logging

import click
import fastavro
import pandas as pd
from cron_descriptor import get_description  # type: ignore
from faker import Faker
from pyarrow import parquet as pq  # type: ignore
import pyarrow as pa  # type: ignore
import rich
from rich.panel import Panel
from rich.table import Table

from hckr.utils.DataUtils import safe_faker_method, print_df_as_table
from hckr.utils.FileUtils import (
    validate_file_extension,
    get_file_format_from_extension,
    FileFormat,
)
from hckr.utils.MessageUtils import success, colored, info, error


@click.group(
    help="cron commands",
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
    help="Output file format, if not provided it gets inferred from file extension",
    required=False,
)
def faker(count, schema, output, format):
    if not format:
        format = get_file_format_from_extension(output)
        info(
            f"File format is not passed, inferring from output file path {colored(output, 'yellow')}"
        )
    else:
        format = format.upper()
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
        error(f"Invalid file format, Available {FileFormat.validFormats()}")
        exit(1)
    info(
        f"Generating {colored(count, 'magenta')} rows in {colored(format, 'yellow')} format."
    )
    logging.debug(f"Data head:\n'{df.head()}'")

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


#
# @data.command()
# @click.option(
#     "-f",
#     "--file",
#     help="File to peek into.",
#     required=True
# )
# @click.option(
#     "-c",
#     "--count",
#     default=10,
#     help="Number of rows to show.",
#     required=False,
# )
# def peek(file, count):
#     info(
#         f"Peeking {colored(count,'magenta')} rows in {colored(file, 'yellow')}"
#     )
#     with open(schema, "r") as schema_file:
#         schema = json.load(schema_file)
#
#     data = []
#
#     # Adjusted fake data generation
#     logging.debug(f"Data head:\n'{df.head()}'")
#     df = readFile
#     print_df_as_table(df)
#     success(f"Data written to {colored(output,'magenta')} in {format} format.")
#
#     rich.print(
#         Panel(
#             output,
#             expand=True,
#             title="File Output",
#         )
#     )

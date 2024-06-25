import logging

import fastavro
import pandas as pd
import rich
from pyarrow import parquet as pq  # type: ignore
from rich.table import Table
import json

from hckr.utils.FileUtils import FileFormat
from hckr.utils.MessageUtils import error, colored, warning, info


def safe_faker_method(faker_instance, method_name, *args):
    """Safely get the Faker method by name and execute it with arguments."""
    if hasattr(faker_instance, method_name):
        method = getattr(faker_instance, method_name)
        return method(*args)
    else:
        raise ValueError(f"No such Faker method: {method_name}")


def print_df_as_table(df, title="Data Sample", count=3):
    MAX_COLS_TO_SHOW = 10
    ROWS_TO_SHOW = min(count, df.shape[0])
    COLS_TO_SHOW = min(MAX_COLS_TO_SHOW, df.shape[1])
    table = Table(
        show_header=True,
        title=title,
        header_style="bold magenta",
        expand=True,
        show_lines=True,  # show line after every row
    )
    table.border_style = "yellow"
    for column in df.columns[:COLS_TO_SHOW]:
        table.add_column(column, no_wrap=False, overflow="fold")
    msg = f"Data has total {colored(df.shape[0], 'yellow')} rows and {colored(df.shape[1], 'yellow')} columns, showing first {colored(ROWS_TO_SHOW, 'yellow')} rows"
    if len(df.columns) > MAX_COLS_TO_SHOW:
        warning(f"{msg} and {colored(COLS_TO_SHOW, 'yellow')} columns")
    else:
        info(msg)
    # Add rows to the table
    for index, row in df.head(count).iterrows():
        # Convert each row to string format, necessary to handle different data types
        table.add_row(*[str(item) for item in row.values[:MAX_COLS_TO_SHOW]])
    rich.print(table)


# Try to read as simple JSON if there is an Error then tries as json lines
def readJSON(_file):
    try:
        return pd.read_json(_file)
    except Exception as e:
        logging.debug(
            f"Error occurred while reading as JSON Object\n{e}\nTrying as JSON Lines"
        )
        df = pd.read_json(_file, lines=True)
        info(f"Data is in {colored('JSON Lines', 'yellow')} format")
        return df


def readFile(_format, FILE):
    try:
        if _format == FileFormat.CSV:
            df = pd.read_csv(FILE)
        elif _format == FileFormat.JSON:
            df = readJSON(FILE)
        elif _format == FileFormat.EXCEL:
            df = pd.read_excel(FILE, engine="openpyxl")
        elif _format == FileFormat.PARQUET:
            df = pq.read_table(FILE).to_pandas()
        elif _format == FileFormat.AVRO:
            with open(FILE, "rb") as f:
                avro_reader = fastavro.reader(f)
                records = [record for record in avro_reader]
            df = pd.DataFrame(records)
        else:
            error(
                f"Invalid file format {colored(str(_format), 'bold yellow')}, Available formats: {colored(FileFormat.validFormats(), 'magenta')}"
            )
            exit(1)
        # print_df_as_table(df, title="Test Read Sample")
        return df
    except Exception as e:
        raise e

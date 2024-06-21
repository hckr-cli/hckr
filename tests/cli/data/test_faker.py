from pathlib import Path

import fastavro
from click.testing import CliRunner

from hckr.cli.data import faker
import pandas as pd
from pyarrow import parquet as pq  # type: ignore
import pyarrow as pa  # type: ignore

from hckr.utils.DataUtils import print_df_as_table
from hckr.utils.FileUtils import delete_path_if_exists

parent_directory = Path(__file__).parent.parent

SCHEMA_FILE = parent_directory / "resources" / "data" / "faker" / "schema.json"
OUTPUT_DIR = parent_directory / "resources" / "data" / "faker" / "output"


# POSITIVE


def readFile(_format, FILE):
    if _format == "csv":
        df = pd.read_csv(FILE)
    elif _format == "json":
        df = pd.read_json(FILE)
    elif _format == "excel":
        df = pd.read_excel(FILE, engine="openpyxl")
    elif _format == "parquet":
        df = pq.read_table(FILE).to_pandas()
    elif _format == "avro":
        with open(FILE, "rb") as f:
            avro_reader = fastavro.reader(f)
            records = [record for record in avro_reader]
        df = pd.DataFrame(records)
    else:
        raise Exception("Invalid _format")
    print_df_as_table(df, title="Test Read Sample")
    return df


def faker_test_util(_format=None, _count=None, _file=None):
    runner = CliRunner()
    DEFAULT_FORMAT = "json"
    DEFAULT_COUNT = 10
    if _file:
        FILE = _file
    else:
        FILE = OUTPUT_DIR / f"output.{_format if _format else DEFAULT_FORMAT}"
    delete_path_if_exists(FILE)
    if _format and _count:
        result = runner.invoke(
            faker, ["-s", SCHEMA_FILE, "-o", FILE, "-c", _count, "-f", _format]
        )
        assert f"Generating {_count} rows in {_format} format" in result.output
        # only validate count if we are checking valid case
        if result.exit_code == 0:
            df = readFile(_format, FILE)
            assert df.shape[0] == _count

    elif _count:
        result = runner.invoke(faker, ["-s", SCHEMA_FILE, "-o", FILE, "-c", _count])
        assert f"Generating {_count} rows in {DEFAULT_FORMAT} format" in result.output
        if result.exit_code == 0:
            df = readFile(DEFAULT_FORMAT, FILE)
            assert df.shape[0] == _count

    elif _format:
        result = runner.invoke(faker, ["-s", SCHEMA_FILE, "-o", FILE, "-f", _format])
        assert f"Generating {DEFAULT_COUNT} rows in {_format} format" in result.output
        if result.exit_code == 0:
            df = readFile(_format, FILE)
            assert df.shape[0] == DEFAULT_COUNT

    else:
        result = runner.invoke(faker, ["-s", SCHEMA_FILE, "-o", FILE])
        assert (
            f"Generating {DEFAULT_COUNT} rows in {DEFAULT_FORMAT} format"
            in result.output
        )
        if result.exit_code == 0:
            df = readFile(DEFAULT_FORMAT, FILE)
            assert df.shape[0] == DEFAULT_COUNT

    print(result.output)
    return result


def test_data_faker_default_count_default_format():
    result = faker_test_util()
    assert result.exit_code == 0


def test_data_faker_given_count():
    result = faker_test_util(_count=20)
    assert result.exit_code == 0


def test_data_faker_given_format():
    result = faker_test_util(_format="csv")
    assert result.exit_code == 0


def test_data_faker_given_count_given_format():
    result = faker_test_util(_format="csv", _count=30)
    assert result.exit_code == 0


def test_data_faker_excel_valid_file_extension():
    FORMATS = ["xls", "xlsx"]
    for _format in FORMATS:
        FILE = OUTPUT_DIR / f"output.{_format}"
        result = faker_test_util(_format="excel", _file=FILE)
        assert result.exit_code == 0


def test_data_faker_parquet_format():
    result = faker_test_util(_format="parquet", _count=30)
    assert result.exit_code == 0


def test_data_faker_avro_format():
    result = faker_test_util(_format="avro", _count=30)
    assert result.exit_code == 0


# NEGATIVE
def test_data_faker_no_schema():
    runner = CliRunner()
    result = runner.invoke(faker, [])
    print(result.output)
    assert "Error: Missing option '-s' / '--schema'" in result.output


def test_data_faker_no_output():
    runner = CliRunner()
    result = runner.invoke(faker, ["-s", SCHEMA_FILE])
    print(result.output)
    assert "Error: Missing option '-o' / '--output'" in result.output


def test_data_faker_invalid_output():
    runner = CliRunner()
    result = runner.invoke(
        faker, ["-s", SCHEMA_FILE, "-o", OUTPUT_DIR, "-f", "INVALID"]
    )
    print(result.output)
    assert (
        "Error: Invalid value for '-f' / '--format': 'INVALID' is not one of 'csv', 'json', 'excel', 'parquet', 'avro'."
        in result.output
    )


def test_data_faker_excel_invalid_file_extension():
    result = faker_test_util(_format="excel")
    # In util default file path is '/tests/cli/resources/data/faker/output/output.excel'
    assert "Invalid file extension: .excel" in result.output
    assert "allowed: ['.xlsx', '.xls']" in result.output

from pathlib import Path

import pyarrow as pa  # type: ignore
from click.testing import CliRunner
from pyarrow import parquet as pq  # type: ignore

from hckr.cli.data import faker
from hckr.utils.DataUtils import readFile
from hckr.utils.FileUtils import (
    delete_path_if_exists,
    FileFormat,
)

parent_directory = Path(__file__).parent.parent

SCHEMA_FILE = parent_directory / "resources" / "data" / "faker" / "schema.json"
OUTPUT_DIR = parent_directory / "resources" / "data" / "faker" / "output"


# POSITIVE


def faker_test_util_format_count(_format, _count=None):
    runner = CliRunner()
    DEFAULT_COUNT = 10
    # create a output file according to format given
    FILE = (
        OUTPUT_DIR / f"output.{'xlsx' if _format == str(FileFormat.EXCEL) else _format}"
    )

    delete_path_if_exists(FILE)
    if _count:
        result = runner.invoke(faker, ["-s", SCHEMA_FILE, "-o", FILE, "-c", _count])
        # make sure format is rightly inferred
        assert f"Generating {_count} rows in {_format} format" in result.output
        # only validate count if we are checking valid case
        if result.exit_code == 0:
            df = readFile(_format, FILE)
            assert df.shape[0] == _count
    else:  # if count  not given use default count
        result = runner.invoke(faker, ["-s", SCHEMA_FILE, "-o", FILE])
        assert (
            "File format is not passed, inferring from output file path"
            in result.output
        )
        assert f"Format inferred: {_format}" in result.output
        assert (
            f"Generating {DEFAULT_COUNT} rows in {str(_format)} format" in result.output
        )
        if result.exit_code == 0:
            df = readFile(_format, FILE)
            assert df.shape[0] == DEFAULT_COUNT

    print(result.output)
    return result


def test_data_faker_inferred_format():
    formats = FileFormat.validFormats()
    for _format in formats:
        print(f"Running for {_format}")
        result = faker_test_util_format_count(_format=_format)
        assert result.exit_code == 0
        print(f"=" * 50)


def test_data_faker_given_count():
    result = faker_test_util_format_count(_count=20, _format=str(FileFormat.CSV))
    assert result.exit_code == 0


def test_data_faker_given_format():
    result = faker_test_util_format_count(_format=str(FileFormat.CSV))
    assert result.exit_code == 0


def test_data_faker_given_count_given_format():
    result = faker_test_util_format_count(_format=str(FileFormat.CSV), _count=30)
    assert result.exit_code == 0


def test_data_faker_parquet_format():
    result = faker_test_util_format_count(_format=str(FileFormat.PARQUET), _count=30)
    assert result.exit_code == 0


def test_data_faker_avro_format():
    result = faker_test_util_format_count(_format=str(FileFormat.AVRO), _count=30)
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


def test_data_faker_invalid_output_format():
    runner = CliRunner()
    result = runner.invoke(
        faker, ["-s", SCHEMA_FILE, "-o", OUTPUT_DIR, "-f", "INVALID"]
    )
    print(result.output)
    assert (
        """Invalid file format invalid, Available ['csv', 'avro', 'json', 'excel', 
'parquet']"""
        in result.output
    )


def test_data_faker_excel_invalid_file_extension():
    runner = CliRunner()
    result = runner.invoke(faker, ["-s", SCHEMA_FILE, "-o", "invalid.excel"])

    print(result.output)
    assert result.exit_code == 1
    assert (
        """Invalid file extension .excel for file invalid.excel, 
Available extensions ['.avro', '.csv', '.json', '.parquet', '.xls', '.xlsx']
Or Please provide format using -f / --format option"""
        in result.output
    )


def test_data_faker_invalid_faker_provider():
    INVALID_SCHEMA_FILE = (
        parent_directory / "resources" / "data" / "faker" / "invalid_schema.json"
    )

    runner = CliRunner()
    result = runner.invoke(faker, ["-s", INVALID_SCHEMA_FILE, "-o", "output.csv"])

    print(result.output)
    assert """No such Faker method: credit_card_invalid""" in result.output


def test_data_faker_schema_file_not_found():
    runner = CliRunner()
    result = runner.invoke(faker, ["-s", "not_found.json", "-o", "output.csv"])

    print(result.output)
    assert (
        """Error: Invalid value for '-s' / '--schema': Path 'not_found.json' does not exist."""
        in result.output
    )

from pathlib import Path

import pyarrow as pa  # type: ignore
from click.testing import CliRunner
from pyarrow import parquet as pq  # type: ignore

from hckr.cli.data import peek
from hckr.utils.FileUtils import (
    FileFormat,
)

parent_directory = Path(__file__).parent.parent

INPUT_DIR = parent_directory / "resources" / "data" / "peek"
INPUT_CSV_FILE = INPUT_DIR / "input.csv"


def peekUtil(_format, _count=None):
    runner = CliRunner()
    DEFAULT_COUNT = 10
    FILE = (
        INPUT_DIR / f"input.{'xlsx' if _format == str(FileFormat.EXCEL) else _format}"
    )
    print(f"Reading from file :{FILE}")
    if _count:
        result = runner.invoke(peek, ["-i", FILE, "-c", _count])
        # print(result.output)
        # make sure format is rightly inferred
        # only validate count if we are checking valid case
        assert f"File format is not passed, inferring from file path" in result.output
        assert f"Peeking {_count} rows in file" in result.output
        assert f"Format inferred: {_format}" in result.output
    else:  # if count  not given use default count
        result = runner.invoke(peek, ["-i", FILE])
        # print(result.output)

        assert f"File format is not passed, inferring from file path" in result.output
        assert f"Peeking {DEFAULT_COUNT} rows in file" in result.output
        assert f"Format inferred: {_format}" in result.output

    print(result.output)
    return result


# POSITIVE
def test_data_peek_inferred_format_default_count():
    formats = FileFormat.validFormats()
    for _format in formats:
        print(f"Running for {_format}")
        result = peekUtil(_format=_format)
        assert result.exit_code == 0
        print(f"=" * 50)


def test_data_peek_inferred_format_given_count():
    formats = FileFormat.validFormats()
    for _format in formats:
        print(f"Running for {_format}")
        result = peekUtil(_format=_format, _count=8)
        # print(result.output)
        assert result.exit_code == 0
        assert "showing first 8 rows" in result.output
        print(f"=" * 50)


def test_data_peek_with_large_cols():
    runner = CliRunner()
    result = runner.invoke(peek, ["-i", INPUT_DIR / "Account.csv"])
    print(result.output)
    assert (
        "Data has total 13 rows and 61 columns, showing first 10 rows and 10 columns"
        in result.output
    )


def test_data_peek_with_json_lines():
    runner = CliRunner()

    result = runner.invoke(peek, ["-i", INPUT_DIR / "json-lines.json"])
    print(result.output)
    assert "Data is in JSON Lines format" in result.output
    assert "Data has total 3 rows and 4 columns, showing first 3 rows" in result.output


# NEGATIVE
def test_data_peek_no_input():
    runner = CliRunner()
    result = runner.invoke(peek, [])
    print(result.output)
    assert "Missing option '-i' / '--input'" in result.output


def test_data_peek_with_incompatible_format():
    runner = CliRunner()
    # giving CSV file but Format as AVRO
    result = runner.invoke(peek, ["-i", INPUT_CSV_FILE, "-f", str(FileFormat.AVRO)])
    print(result.output)
    assert "Some error occurred while reading data" in result.output


def test_data_peek_with_invalid_input_file_format():
    runner = CliRunner()
    INVALID_FORMAT = "dvs"
    # giving CSV file but Format as AVRO
    result = runner.invoke(peek, ["-i", INPUT_CSV_FILE, "-f", INVALID_FORMAT])
    print(result.output)
    assert (
        f"""Invalid file format {INVALID_FORMAT}, Available formats: ['csv', 'avro', 'json', 'excel', 
'parquet']"""
        in result.output
    )


def test_data_peek_with_input_file_not_found():
    runner = CliRunner()
    # giving CSV file but Format as AVRO
    result = runner.invoke(peek, ["-i", "invalid.csv"])
    print(result.output)
    assert "Some error occurred while reading data" in result.output
    assert "[Errno 2] No such file or directory: 'invalid.csv" in result.output

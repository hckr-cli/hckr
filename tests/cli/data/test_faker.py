from pathlib import Path

from click.testing import CliRunner

from hckr.cli.data import faker

parent_directory = Path(__file__).parent.parent

SCHEMA_FILE = parent_directory / "resources" / "data" / "faker" / "schema.json"
OUTPUT_FILE_JSON = parent_directory / "resources" / "data" / "faker" / "output.csv"

# POSITIVE


def test_data_faker_default_count():
    runner = CliRunner()
    result = runner.invoke(faker, ["-s", SCHEMA_FILE, "-o", OUTPUT_FILE_JSON])
    print(result.output)
    # assert (
    #         "Error: Missing option '-o' / '--output'"
    #         in result.output
    # )


# NEGATIVE


def test_data_faker_no_schema():
    runner = CliRunner()
    result = runner.invoke(faker, [])
    # print(result.output)
    assert "Error: Missing option '-s' / '--schema'" in result.output


def test_data_faker_no_output():
    runner = CliRunner()
    result = runner.invoke(faker, ["-s", SCHEMA_FILE])
    print(result.output)
    assert "Error: Missing option '-o' / '--output'" in result.output


def test_data_faker_invalid_output():
    runner = CliRunner()
    result = runner.invoke(
        faker, ["-s", SCHEMA_FILE, "-o", OUTPUT_FILE_JSON, "-f", "INVALID"]
    )
    print(result.output)
    assert (
        "Error: Invalid value for '-f' / '--format': 'INVALID' is not one of 'csv', 'json', 'excel', 'parquet', 'avro'."
        in result.output
    )

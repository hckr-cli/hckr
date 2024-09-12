from click.testing import CliRunner

from hckr.cli.db import query
from hckr.cli.configure import configure_db
from tests.testUtils import _get_args_with_config_path


def _run_query_and_assert(cli_runner, sql_query, value_assert=None):
    result = cli_runner.invoke(
        query, _get_args_with_config_path([sql_query, "-c", "testdb_sqlite"])
    )
    print(result.output)
    if value_assert:
        assert value_assert in result.output


def test_db_query_sqlite(cli_runner, sqlite_options):
    # # configuring sqlite for testing
    result = cli_runner.invoke(configure_db, sqlite_options)
    assert result.exit_code == 0
    assert "Database configuration saved successfully" in result.output
    assert "[testdb_sqlite]" in result.output

    _run_query_and_assert(cli_runner, "drop table if exists users")

    _run_query_and_assert(
        cli_runner,
        """
                              CREATE TABLE users (
                              id INTEGER PRIMARY KEY,
                              name TEXT NOT NULL,
                              email TEXT NOT NULL UNIQUE
                              );
                              """,
    )

    _run_query_and_assert(
        cli_runner,
        "INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');",
    )

    _run_query_and_assert(cli_runner, "select * from users;")


# NEGATIVE USE CASES


def test_db_query_missing_config():
    runner = CliRunner()
    result = runner.invoke(
        query, _get_args_with_config_path(["select 1", "-c", "INVALID"])
    )
    print(result.output)
    assert result.exit_code != 0
    assert "Config INVALID is not present in the config file" in result.output


def test_db_query_invalid_config():
    runner = CliRunner()
    result = runner.invoke(
        query, _get_args_with_config_path(["select 1", "-c", "CUSTOM"])
    )
    # print(result.output)
    print(result.stdout)
    assert result.exit_code != 0
    assert "The configuration CUSTOM is not database type" in result.output


def test_db_query_missing_query():
    runner = CliRunner()
    result = runner.invoke(query, _get_args_with_config_path([]))
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing argument 'QUERY'" in result.output

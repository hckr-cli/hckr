from hckr.cli.configure import configure_db, set_default
from hckr.cli.db import query
from hckr.utils.config.ConfigUtils import list_config
from tests.testUtils import _get_args_with_config_path, TEST_HCKRCFG_FILE


def test_configure_postgres(cli_runner, postgres_options):
    result = cli_runner.invoke(configure_db, postgres_options)
    print(result.output)
    assert result.exit_code == 0
    assert "Database configuration saved successfully" in result.output
    assert "[testdb_postgres]" in result.output


def test_configure_mysql(cli_runner, mysql_options):
    result = cli_runner.invoke(configure_db, mysql_options)
    print(result.output)
    assert result.exit_code == 0
    assert "Database configuration saved successfully" in result.output
    assert "[testdb_mysql]" in result.output


def test_configure_snowflake(cli_runner, snowflake_options):
    result = cli_runner.invoke(configure_db, snowflake_options)
    print(result.output)
    assert result.exit_code == 0
    assert "Database configuration saved successfully" in result.output
    assert "[testdb_snowflake]" in result.output


def test_configure_sqlite(cli_runner, sqlite_options):
    result = cli_runner.invoke(configure_db, sqlite_options)
    print(result.output)
    assert result.exit_code == 0
    assert "Database configuration saved successfully" in result.output
    assert "[testdb_sqlite]" in result.output


def test_configure_set_default_db(cli_runner, sqlite_options):
    # first we have to configure a sqlite database
    result = cli_runner.invoke(configure_db, sqlite_options)
    assert result.exit_code == 0
    assert "Database configuration saved successfully" in result.output
    assert "[testdb_sqlite]" in result.output

    result = cli_runner.invoke(
        set_default, _get_args_with_config_path(["database", "testdb_sqlite"])
    )
    print(result.output)
    assert result.exit_code == 0
    assert "Default config for database configured" in result.output

    # query with default config
    result = cli_runner.invoke(query, _get_args_with_config_path(["select 1"]))
    print(result.output)
    assert result.exit_code == 0
    assert (
        "Default database config testdb_sqlite inferred from [DEFAULT] config"
        in result.output
    )


def test_configure_set_default_missing_arg(cli_runner):
    result = cli_runner.invoke(set_default, _get_args_with_config_path([]))
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing argument '{database}'" in result.output


def test_configure_set_default_invalid_arg(cli_runner):
    result = cli_runner.invoke(set_default, _get_args_with_config_path(["invalid"]))
    print(result.output)
    assert result.exit_code != 0
    assert (
        "Error: Invalid value for '{database}': 'invalid' is not 'database'."
        in result.output
    )

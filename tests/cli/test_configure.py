from hckr.cli.configure import configure_db
from hckr.utils.MessageUtils import _PMsg, PInfo


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


def test_test():
    hi = "ashish"
    PInfo(f"hello {hi}")

# SPDX-FileCopyrightText: 2024-present Ashish Patel <ashishpatel0720@gmail.com>
#
# SPDX-License-Identifier: MIT
from pathlib import Path

import pytest
from click.testing import CliRunner

from hckr.utils.config.ConfigUtils import init_config

current_directory = Path(__file__).parent
SQLITE_DB = current_directory / "cli" / "resources" / "db" / "test_db.sqlite"


@pytest.fixture(scope="package")
def local_sqlite_db():
    return SQLITE_DB


@pytest.fixture(scope="package")
def cli_runner():
    init_config(overwrite=True)  # recreate the config file
    return CliRunner()


@pytest.fixture(scope="package")
def postgres_options():
    return [
        "--config-name",
        "testdb_postgres",
        "--database-type",
        "1",
        "--user",
        "user",
        "--password",
        "password",
        "--host",
        "host.postgres",
        "--port",
        "11143",
        "--database-name",
        "defaultdb",
    ]


@pytest.fixture(scope="package")
def mysql_options():
    return [
        "--config-name",
        "testdb_mysql",
        "--database-type",
        "2",
        "--user",
        "user",
        "--password",
        "password",
        "--host",
        "host",
        "--port",
        "123",
        "--database-name",
        "defaultdb",
    ]


@pytest.fixture(scope="package")
def snowflake_options():
    return [
        "--config-name",
        "testdb_snowflake",
        "--database-type",
        "4",
        "--user",
        "user",
        "--password",
        "password",
        "--database-name",
        "database",
        "--schema",
        "PUBLIC",
        "--account",
        "account-id",
        "--warehouse",
        "COMPUTE_WH",
        "--role",
        "ACCOUNTADMIN",
    ]


@pytest.fixture(scope="package")
def sqlite_options():
    return [
        "--config-name",
        "testdb_sqlite",
        "--database-type",
        "3",
        "--database-name",
        f"{SQLITE_DB}",
    ]

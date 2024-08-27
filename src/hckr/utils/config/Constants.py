from enum import Enum
from pathlib import Path

config_path = Path.home() / ".hckrcfg"
DEFAULT_CONFIG = "DEFAULT"


class DBType(str, Enum):
    PostgreSQL = ("PostgreSQL",)
    MySQL = ("MySQL",)
    SQLite = ("SQLite",)
    Snowflake = ("Snowflake",)

    def __str__(self):
        return self.value


class ConfigType(str, Enum):
    DATABASE = ("database",)

    def __str__(self):
        return self.value


db_type_mapping = {
    "1": DBType.PostgreSQL,
    "2": DBType.MySQL,
    "3": DBType.SQLite,
    "4": DBType.Snowflake,
}

# =============== CONFIG CONSTANTS =================== #
# COMMON CONFIG Constants
CONFIG_TYPE = "config_type"

# DATABASE CONFIG Constants
DB_TYPE = "type"
DB_HOST = "host"
DB_PORT = "port"
DB_USER = "username"
DB_PASSWORD = "password"

DB_NAME = "database"
DB_SCHEMA = "schema"

# SNOWFLAKE SPECIFIC
DB_ACCOUNT = "account"
DB_ROLE = "role"
DB_WAREHOUSE = "warehouse"

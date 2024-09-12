from pathlib import Path

current_directory = Path(__file__).parent
SQLITE_DB = current_directory / "cli" / "resources" / "db" / "test_db.sqlite"
TEST_HCKRCFG_FILE = current_directory / "cli" / "resources" / "config" / ".hckrcfg"


def _get_args_with_config_path(args):
    args.extend(["--config-path", str(TEST_HCKRCFG_FILE)])
    return args

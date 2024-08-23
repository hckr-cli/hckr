import string
from distutils.command.config import config
import random
from click.testing import CliRunner

from hckr.cli.configure import set, get


def _get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


# DEFAULT CONFIG GET AND SET
def test_configure_get_set_default():
    runner = CliRunner()
    _key = f"key_{_get_random_string(5)}"
    _value = f"value_{_get_random_string(5)}"
    result = runner.invoke(set, [_key, _value])
    assert result.exit_code == 0
    print(result.output)

    assert (
        f"Set [DEFAULT] {_key} = {_value}"
        in result.output
    )
    result = runner.invoke(get, [_key, _value])

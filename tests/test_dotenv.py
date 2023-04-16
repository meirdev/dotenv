import logging
import os

import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

import dotenv


def test_parse():
    assert dotenv.parse("FOO=bar") == {"FOO": "bar"}

    assert dotenv.parse("FOO='bar'") == {"FOO": "bar"}
    assert dotenv.parse('FOO="bar"') == {"FOO": "bar"}
    assert dotenv.parse("FOO=`bar`") == {"FOO": "bar"}

    assert dotenv.parse("FOO=bar\nBAR=baz") == {"FOO": "bar", "BAR": "baz"}
    assert dotenv.parse("FOO=bar\rBAR=baz") == {"FOO": "bar", "BAR": "baz"}
    assert dotenv.parse("FOO=bar\r\nBAR=baz") == {"FOO": "bar", "BAR": "baz"}

    assert dotenv.parse("FOO='bar # baz'") == {"FOO": "bar # baz"}
    assert dotenv.parse("FOO=bar # baz") == {"FOO": "bar"}

    assert dotenv.parse("FOO=   bar   ") == {"FOO": "bar"}
    assert dotenv.parse('FOO="   bar   "') == {"FOO": "   bar   "}


def test_config(fs):
    fs.create_file(".env", contents="DOTENV_TEST_VAR=ok")

    dotenv.config()

    assert os.environ["DOTENV_TEST_VAR"] == "ok"


def test_config_with_path(fs):
    fs.create_file("/home/dir/.env", contents="DOTENV_TEST_VAR=ok")

    dotenv.config(path="/home/dir/.env")

    assert os.environ["DOTENV_TEST_VAR"] == "ok"


def test_config_with_override(fs):
    os.environ["DOTENV_TEST_VAR"] == "ok"

    fs.create_file(".env", contents="DOTENV_TEST_VAR=yes")

    dotenv.config()

    assert os.environ["DOTENV_TEST_VAR"] == "ok"

    dotenv.config(override=True)

    assert os.environ["DOTENV_TEST_VAR"] == "yes"


def test_config_with_raise_error(fs):
    with pytest.raises(OSError):
        dotenv.config(raise_error=True)


def test_config_with_debug(caplog):
    with caplog.at_level(logging.DEBUG, logger="dotenv"):
        dotenv.config(path="/non-exists-path/.env")

        for record in caplog.records:
            assert "Failed to load /non-exists-path/.env" in record.message


def test_config_with_debug_and_override(caplog, fs):
    fs.create_file(".env", contents="OVERWRITE_ME=foo")

    os.environ["OVERWRITE_ME"] = "-"

    with caplog.at_level(logging.DEBUG, logger="dotenv"):
        dotenv.config()
        dotenv.config(override=True)

    for record, message in zip(
        caplog.records,
        (
            "'OVERWRITE_ME' is already defined in `os.environ` and was NOT overwritten",
            "'OVERWRITE_ME' is already defined in `os.environ` and WAS overwritten",
        ),
    ):
        assert message in record.message

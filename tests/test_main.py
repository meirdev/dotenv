import sys
import tempfile

from pyfakefs.fake_filesystem_unittest import Patcher

from dotenv.__main__ import main


def test_main():
    with tempfile.NamedTemporaryFile() as tmp:
        sys.argv = ["dotenv", f"printenv > {tmp.name}"]

        with Patcher() as patcher:
            patcher.fs.create_file(".env", contents="IT_WORKS_CLI=yes")

            main()

        assert "IT_WORKS_CLI=yes" in tmp.read().decode()

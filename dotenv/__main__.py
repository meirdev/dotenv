import argparse
import logging
import os
import subprocess
import sys

import dotenv


def main() -> None:
    arg_parser = argparse.ArgumentParser("Dotenv")
    arg_parser.add_argument(
        "--dotenv_config_path", default=os.environ.get("DOTENV_CONFIG_PATH")
    )
    arg_parser.add_argument(
        "--dotenv_config_encoding",
        action="store_true",
        default=os.environ.get("DOTENV_CONFIG_ENCODING"),
    )
    arg_parser.add_argument(
        "--dotenv_config_override",
        action="store_true",
        default=os.environ.get("DOTENV_CONFIG_OVERRIDE", False),
    )
    arg_parser.add_argument(
        "--dotenv_config_debug",
        action="store_true",
        default=os.environ.get("DOTENV_CONFIG_DEBUG", False),
    )

    args, command = arg_parser.parse_known_args()

    if args.dotenv_config_debug:
        logging.basicConfig(
            format="[%(name)s] [%(levelname)s] %(message)s",
            stream=sys.stdout,
            level=logging.DEBUG,
        )

    dotenv.config(
        path=args.dotenv_config_path,
        encoding=args.dotenv_config_encoding,
        override=args.dotenv_config_override,
    )

    subprocess.run(command, shell=True)


if __name__ == "__main__":
    main()

import logging
import os
import re

logger = logging.getLogger("dotenv")

LINE = re.compile(
    r"""(?:^|^)\s*(?:export\s+)?([\w.-]+)(?:\s*=\s*?|:\s+?)(\s*'(?:\\'|[^'])*'|\s*"(?:\\"|[^"])*"|\s*`(?:\\`|[^`])*`|[^#\r\n]+)?\s*(?:#.*)?(?:$|$)""",
    re.MULTILINE | re.DOTALL,
)


def parse(src: str) -> dict[str, str]:
    obj = {}

    # Convert line breaks to same format
    src = re.sub(r"\r\n?", "\n", src)

    for match in re.findall(LINE, src):
        key, value = match

        value = value.strip()

        # Check if double quoted
        is_quoted = value and value[0] == '"'

        # Remove surrounding quotes
        value = re.sub(r"""^(['"`])([\s\S]*)\1$""", r"\2", value)

        # Expand newlines if double quoted
        if is_quoted:
            value = value.replace(r"\n", "\n").replace(r"\r", "\r")

        obj[key] = value

    return obj


def config(
    path: str | None = None,
    encoding: str | None = None,
    override: bool = False,
    raise_error: bool = False,
) -> None:
    if path is None:
        path = os.path.join(os.getcwd(), ".env")
    else:
        path = os.path.expanduser(path)

    try:
        with open(path, encoding=encoding) as fp:
            parsed = parse(fp.read())

            for key, value in parsed.items():
                key_defined = key in os.environ

                if key not in os.environ or override:
                    os.environ[key] = value

                if key_defined:
                    logger.debug(
                        f"{key!r} is already defined in `os.environ` and {'WAS' if override else 'was NOT'} overwritten"
                    )

    except Exception as error:
        logger.debug(f"Failed to load {path} {error}")

        if raise_error:
            raise

"""Configuration — TOML, INI files, environment variables, and layering them.

Settings such as a port number or a debug flag should live outside the code,
so the same program can run on a laptop, in CI and in production. The
standard library reads the common formats:

    tomllib        TOML (pyproject.toml uses it); typed values, nested tables.
                   Read-only: the standard library cannot write TOML.
    configparser   INI files: [sections] of key = value, every value a string
    os.environ     environment variables, always strings, often missing

Real programs combine sources in layers, each overriding the one before:

    built-in defaults  <  config file  <  environment  <  command line

so a file sets the usual values and one environment variable can change a
single setting for one run.
"""

import tempfile
import tomllib
from pathlib import Path


TOML_TEXT = """
title = "Inventory service"
debug = false

[server]
host = "127.0.0.1"
port = 8080
workers = [1, 2, 4]

[database]
url = "sqlite:///inventory.db"
timeout = 2.5
"""


def toml_demo() -> None:
    config = tomllib.loads(TOML_TEXT)
    # TOML values arrive with real types: no int("8080") needed.
    port = config["server"]["port"]
    print(f"title={config['title']!r}, debug={config['debug']}")
    print(f"port {port} is an {type(port).__name__}, "
          f"workers={config['server']['workers']}")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "settings.toml"
        path.write_text(TOML_TEXT, encoding="utf-8")
        # tomllib.load needs the file opened in *binary* mode ("rb").
        with path.open("rb") as f:
            from_file = tomllib.load(f)
    print(f"from a file, database timeout = {from_file['database']['timeout']}")

    try:
        tomllib.loads("port = 80 80")
    except tomllib.TOMLDecodeError as exc:
        print(f"TOMLDecodeError: {exc}")


def main() -> None:
    toml_demo()


if __name__ == "__main__":
    main()

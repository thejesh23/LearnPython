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

import configparser
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


INI_TEXT = """
[DEFAULT]
timeout = 30

[server]
host = 0.0.0.0
port = 8000
debug = yes

[backup]
enabled = off
"""


def ini_demo() -> None:
    parser = configparser.ConfigParser()
    parser.read_string(INI_TEXT)
    print(f"sections: {parser.sections()}  (DEFAULT is not listed)")

    server = parser["server"]
    # Everything is a string; the get* helpers convert for you.
    print(f"port as stored: {server['port']!r}, getint: {server.getint('port')}")
    print(f"debug = yes -> getboolean: {server.getboolean('debug')}")
    print(f"backup enabled = off -> {parser.getboolean('backup', 'enabled')}")
    # [DEFAULT] values show up in every section.
    print(f"backup timeout inherited from DEFAULT: {parser['backup']['timeout']}")
    print(f"missing key with fallback: {server.get('retries', fallback='3')}")

    # ConfigParser can also write INI files back out.
    parser["server"]["port"] = "9000"
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "app.ini"
        with path.open("w", encoding="utf-8") as f:
            parser.write(f)
        again = configparser.ConfigParser()
        again.read(path, encoding="utf-8")
    print(f"round trip through a file, port = {again['server']['port']}")


def main() -> None:
    toml_demo()
    print()
    ini_demo()


if __name__ == "__main__":
    main()

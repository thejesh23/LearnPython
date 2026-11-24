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
import os
import tempfile
import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import Any


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


def env_int(name: str, default: int, env: Mapping[str, str] = os.environ) -> int:
    raw = env.get(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"{name} must be a whole number, got {raw!r}") from None


def env_bool(name: str, default: bool, env: Mapping[str, str] = os.environ) -> bool:
    raw = env.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def env_demo() -> None:
    # os.environ behaves like a dict of strings. .get() avoids a KeyError
    # when a variable is not set; os.getenv(name, default) is the same thing.
    print(f"HOME is set: {'HOME' in os.environ or 'USERPROFILE' in os.environ}")

    # Passing a dict instead of the real os.environ keeps this demo (and
    # tests) independent of the machine it runs on.
    fake_env = {"APP_PORT": "9090", "APP_DEBUG": "true", "APP_WORKERS": "four"}
    print(f"APP_PORT    -> {env_int('APP_PORT', 8000, fake_env)}")
    print(f"APP_TIMEOUT -> {env_int('APP_TIMEOUT', 30, fake_env)} (default)")
    print(f"APP_DEBUG   -> {env_bool('APP_DEBUG', False, fake_env)}")
    try:
        env_int("APP_WORKERS", 1, fake_env)
    except ValueError as exc:
        print(f"ValueError: {exc}")


DEFAULTS: dict[str, Any] = {"host": "127.0.0.1", "port": 8000, "debug": False}


def from_env(env: Mapping[str, str]) -> dict[str, Any]:
    """Only the variables that are actually set, so the rest fall through."""
    found: dict[str, Any] = {}
    if "APP_PORT" in env:
        found["port"] = env_int("APP_PORT", 0, env)
    if "APP_DEBUG" in env:
        found["debug"] = env_bool("APP_DEBUG", False, env)
    return found


def from_args(args: list[str]) -> dict[str, Any]:
    """A tiny stand-in for argparse: --host=NAME."""
    return {k[2:]: v for k, v in (a.split("=", 1) for a in args)}


def layering_demo() -> None:
    file_layer = tomllib.loads('port = 8080\nhost = "0.0.0.0"\n')
    layers = [
        ("defaults", DEFAULTS),
        ("file", file_layer),
        ("env", from_env({"APP_DEBUG": "1"})),
        ("cli", from_args(["--host=localhost"])),
    ]
    # Later dicts win when keys repeat: d1 | d2 | d3.
    final: dict[str, Any] = {}
    source: dict[str, str] = {}
    for name, layer in layers:
        final |= layer
        source.update(dict.fromkeys(layer, name))
    for key, value in final.items():
        print(f"{key:6} = {value!r:12} from {source[key]}")


def main() -> None:
    toml_demo()
    print()
    ini_demo()
    print()
    env_demo()
    print()
    layering_demo()


if __name__ == "__main__":
    main()

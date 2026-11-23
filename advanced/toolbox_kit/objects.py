"""Class-level tools: a validating descriptor and a typed dataclass config loader."""

import dataclasses
import typing
from collections.abc import Callable, Mapping
from typing import Any


class Field:
    """Data descriptor that type-checks (and optionally range-checks) on every assignment."""

    def __init__(self, kind: type, check: Callable[[Any], bool] | None = None) -> None:
        self.kind, self.check = kind, check

    def __set_name__(self, owner: type, name: str) -> None:
        self.name, self.private = name, f"_{name}"  # no need to repeat the name

    def __get__(self, obj: object | None, objtype: type | None = None) -> Any:
        if obj is None:
            return self  # accessed on the class
        return getattr(obj, self.private)

    def __set__(self, obj: object, value: Any) -> None:
        if not isinstance(value, self.kind):
            raise TypeError(f"{self.name} must be {self.kind.__name__}, "
                            f"got {type(value).__name__}")
        if self.check is not None and not self.check(value):
            raise ValueError(f"{self.name}={value!r} failed validation")
        setattr(obj, self.private, value)


class ConfigError(Exception):
    """A config value is missing, unknown, or cannot be converted."""


_TRUE, _FALSE = {"1", "true", "yes", "on"}, {"0", "false", "no", "off"}


def _coerce(raw: Any, kind: type) -> Any:
    if not isinstance(raw, str) or kind is str:
        return raw
    if kind is bool:
        if raw.lower() in _TRUE | _FALSE:
            return raw.lower() in _TRUE
        raise ValueError(f"not a boolean: {raw!r}")
    if typing.get_origin(kind) is list:
        (item,) = typing.get_args(kind)
        return [_coerce(part.strip(), item) for part in raw.split(",") if part.strip()]
    return kind(raw)  # int("8080"), float("0.5"), Path("/tmp") ...


def load_config[C](cls: type[C], data: Mapping[str, Any], prefix: str = "") -> C:
    """Build dataclass ``cls`` from string-ish data, converting to each field's type.

    With a ``prefix`` (e.g. ``"APP_"`` over ``os.environ``) only matching keys are
    read, and the prefix is stripped and the rest lower-cased to find the field.
    """
    if not dataclasses.is_dataclass(cls):
        raise TypeError(f"{cls.__name__} is not a dataclass")
    hints = typing.get_type_hints(cls)  # resolves string annotations
    names = {f.name for f in dataclasses.fields(cls) if f.init}
    values: dict[str, Any] = {}
    for key, raw in data.items():
        if prefix and not key.startswith(prefix):
            continue
        name = key.removeprefix(prefix).lower() if prefix else key
        if name not in names:
            raise ConfigError(f"unknown setting {key!r}")
        try:
            values[name] = _coerce(raw, hints[name])
        except ValueError as exc:
            raise ConfigError(f"{key}: {exc}") from exc  # keep the original as __cause__
    try:
        return cls(**values)
    except (TypeError, ValueError) as exc:  # a required field is missing, __post_init__ said no
        raise ConfigError(str(exc)) from exc

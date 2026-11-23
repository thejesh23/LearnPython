"""toolbox_kit: timed, retry, describe, Pipeline, Field and load_config.

    >>> from advanced.toolbox_kit import Pipeline, describe
    >>> Pipeline(range(10)).map(lambda n: n * n).filter(lambda n: n % 2).take(3)
    [1, 9, 25]
    >>> describe([7, "hi", None])
    "a list of 3: [the integer 7, the string 'hi', nothing]"
"""

from .functions import Pipeline, RetryError, describe, retry, timed
from .objects import ConfigError, Field, load_config

__all__ = [
    "timed",
    "retry",
    "RetryError",
    "describe",
    "Pipeline",
    "Field",
    "load_config",
    "ConfigError",
]

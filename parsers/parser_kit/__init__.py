"""parser_kit: tokenize, parse and evaluate arithmetic three ways that must agree.

    >>> from parsers.parser_kit import calculate, to_rpn
    >>> calculate("2 ** 3 ** 2 - x", {"x": 12}, via="vm")
    500
    >>> to_rpn("-2 ** 2")
    ['2', '2', '**', 'u-']
"""

from collections.abc import Callable
from typing import Any

from .backends import Env, Instr, compile_tree, eval_rpn, evaluate, infix, run
from .lexer import ParseError, Token, tokenize
from .parser import Binary, Node, Num, Unary, Var, parse, to_rpn

PATHS: dict[str, Callable[[str, Env], Any]] = {
    "tree": lambda source, env: evaluate(parse(source), env),
    "rpn": lambda source, env: eval_rpn(to_rpn(source), env),
    "vm": lambda source, env: run(compile_tree(parse(source)), env),
}

__all__ = [
    "PATHS", "calculate", "ParseError", "Token", "tokenize", "Node", "Num", "Var", "Unary",
    "Binary", "parse", "to_rpn", "evaluate", "infix", "eval_rpn", "Instr", "compile_tree", "run",
]


def calculate(source: str, env: Env | None = None, via: str = "tree") -> Any:
    """Evaluate ``source`` along one path: "tree", "rpn" or "vm"."""
    if via not in PATHS:
        raise ValueError(f"unknown path {via!r}; choose from {sorted(PATHS)}")
    return PATHS[via](source, env or {})

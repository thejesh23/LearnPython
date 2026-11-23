"""Back ends: three ways to get a value out of the same expression.

1. walk the tree (``evaluate``),
2. run the shunting-yard postfix with a stack (``eval_rpn``),
3. compile the tree to bytecode once, then run it on a stack VM (``compile_tree`` + ``run``).
"""

import operator
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from .lexer import ParseError
from .parser import Binary, Node, Num, Unary, Var, number

Env = Mapping[str, Any]

BINARY: dict[str, Callable[[Any, Any], Any]] = {
    "+": operator.add, "-": operator.sub, "*": operator.mul,
    "/": operator.truediv, "%": operator.mod, "**": operator.pow,
}
UNARY: dict[str, Callable[[Any], Any]] = {"-": operator.neg, "+": operator.pos}
OPCODES = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD", "**": "POW"}


def lookup(name: str, env: Env) -> Any:
    """Read a variable, turning a missing one into a clear error."""
    if name not in env:
        raise NameError(f"name {name!r} is not defined")
    return env[name]


def evaluate(node: Node, env: Env | None = None) -> Any:
    """Tree-walking interpreter: evaluate children, then apply the operator."""
    env = env or {}
    match node:
        case Num(value):
            return value
        case Var(name):
            return lookup(name, env)
        case Unary(op, operand):
            return UNARY[op](evaluate(operand, env))
        case Binary(op, left, right):
            return BINARY[op](evaluate(left, env), evaluate(right, env))
    raise TypeError(f"not a node: {node!r}")


def infix(node: Node) -> str:
    """Fully parenthesised source, so the tree's grouping is visible."""
    match node:
        case Num(value):
            return repr(value)
        case Var(name):
            return name
        case Unary(op, operand):
            return f"({op}{infix(operand)})"
        case Binary(op, left, right):
            return f"({infix(left)} {op} {infix(right)})"
    raise TypeError(f"not a node: {node!r}")


def eval_rpn(tokens: list[str], env: Env | None = None) -> Any:
    """Evaluate postfix tokens: operands push, operators pop their arguments."""
    env = env or {}
    stack: list[Any] = []
    for tok in tokens:
        if tok in ("u-", "u+"):
            stack.append(UNARY[tok[1]](stack.pop()))
        elif tok in BINARY:
            b, a = stack.pop(), stack.pop()  # right operand is on top
            stack.append(BINARY[tok](a, b))
        elif tok[0].isdigit() or tok[0] == ".":
            stack.append(number(tok))
        else:
            stack.append(lookup(tok, env))
    if len(stack) != 1:
        raise ParseError("malformed postfix", 0)
    return stack[0]


@dataclass(frozen=True)
class Instr:
    """One VM instruction, e.g. ``Instr("PUSH", 2)`` or ``Instr("ADD")``."""

    op: str
    arg: Any = None

    def __str__(self) -> str:
        return self.op if self.arg is None else f"{self.op} {self.arg!r}"


def compile_tree(node: Node) -> list[Instr]:
    """Emit children first, then the operator: bytecode is the tree in postfix."""
    match node:
        case Num(value):
            return [Instr("PUSH", value)]
        case Var(name):
            return [Instr("LOAD", name)]
        case Unary(op, operand):
            return compile_tree(operand) + [Instr("NEG" if op == "-" else "POS")]
        case Binary(op, left, right):
            return compile_tree(left) + compile_tree(right) + [Instr(OPCODES[op])]
    raise TypeError(f"not a node: {node!r}")


def run(code: list[Instr], env: Env | None = None) -> Any:
    """The VM loop: a flat dispatch over instructions, no parsing at run time."""
    env = env or {}
    by_opcode = {name: BINARY[sym] for sym, name in OPCODES.items()}
    stack: list[Any] = []
    for instr in code:
        if instr.op == "PUSH":
            stack.append(instr.arg)
        elif instr.op == "LOAD":
            stack.append(lookup(instr.arg, env))
        elif instr.op == "NEG":
            stack.append(-stack.pop())
        elif instr.op == "POS":
            stack.append(+stack.pop())
        else:
            b, a = stack.pop(), stack.pop()
            stack.append(by_opcode[instr.op](a, b))
    return stack.pop()

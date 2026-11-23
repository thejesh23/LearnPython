"""Parsers: tokens -> a tree (recursive descent) or postfix (shunting-yard).

Both follow Python's own precedence and associativity, so they must agree.
"""

from collections.abc import Callable
from dataclasses import dataclass

from .lexer import ParseError, Token, tokenize


@dataclass(frozen=True)
class Num:
    """A number literal."""

    value: int | float


@dataclass(frozen=True)
class Var:
    """A variable reference."""

    name: str


@dataclass(frozen=True)
class Unary:
    """A prefix sign applied to one operand."""

    op: str
    operand: "Node"


@dataclass(frozen=True)
class Binary:
    """An infix operator with two operands."""

    op: str
    left: "Node"
    right: "Node"


Node = Num | Var | Unary | Binary


def number(text: str) -> int | float:
    """Python's rule: a dot makes a float, otherwise an int."""
    return float(text) if "." in text else int(text)


def parse(source: str) -> Node:
    """Recursive descent, one function per grammar rule (lowest precedence first)."""
    tokens, pos = tokenize(source), 0

    def take(*texts: str) -> Token | None:
        nonlocal pos
        if tokens[pos].kind == "op" and tokens[pos].text in texts:
            pos += 1
            return tokens[pos - 1]
        return None

    def binary_level(next_level: Callable[[], Node], ops: tuple[str, ...]) -> Node:
        node = next_level()  # left-associative: fold each operand onto the left
        while op := take(*ops):
            node = Binary(op.text, node, next_level())
        return node

    def expr() -> Node:  # expr  := term (('+' | '-') term)*
        return binary_level(term, ("+", "-"))

    def term() -> Node:  # term  := unary (('*' | '/' | '%') unary)*
        return binary_level(unary, ("*", "/", "%"))

    def unary() -> Node:  # unary := ('-' | '+') unary | power
        if op := take("-", "+"):
            return Unary(op.text, unary())
        return power()

    def power() -> Node:  # power := atom ['**' unary]
        base = atom()  # right side recurses into unary: 2 ** -3 ** 2 == 2 ** (-(3 ** 2))
        return Binary("**", base, unary()) if take("**") else base

    def atom() -> Node:  # atom  := number | name | '(' expr ')'
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        if tok.kind == "num":
            return Num(number(tok.text))
        if tok.kind == "name":
            return Var(tok.text)
        if tok.kind == "(":
            node = expr()
            if tokens[pos].kind != ")":
                raise ParseError("expected ')'", tokens[pos].position)
            pos += 1
            return node
        raise ParseError(f"expected a value, found {tok.text or 'end of input'!r}", tok.position)

    tree = expr()
    if tokens[pos].kind != "eof":
        raise ParseError(f"unexpected {tokens[pos].text!r}", tokens[pos].position)
    return tree


PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "u-": 3, "u+": 3, "**": 4}
RIGHT_ASSOC = {"**"}


def to_rpn(source: str) -> list[str]:
    """Shunting-yard: infix to postfix with one operator stack. Unary signs become u-/u+."""
    output: list[str] = []
    stack: list[Token] = []
    expect_operand = True  # the flag that tells unary minus from subtraction
    for tok in tokenize(source):
        if tok.kind in ("num", "name") and expect_operand:
            output.append(tok.text)
            expect_operand = False
        elif tok.kind == "(" and expect_operand:
            stack.append(tok)
        elif tok.kind == ")" and not expect_operand:
            while stack and stack[-1].kind != "(":
                output.append(stack.pop().text)
            if not stack:
                raise ParseError("unbalanced ')'", tok.position)
            stack.pop()
        elif tok.kind == "op" and expect_operand and tok.text in "+-":
            stack.append(Token("op", "u" + tok.text, tok.position))  # prefix: pops nothing
        elif tok.kind == "op" and not expect_operand:
            prec = PRECEDENCE[tok.text]
            while stack and stack[-1].kind == "op" and (
                PRECEDENCE[stack[-1].text] > prec
                or (PRECEDENCE[stack[-1].text] == prec and tok.text not in RIGHT_ASSOC)
            ):
                output.append(stack.pop().text)
            stack.append(tok)
            expect_operand = True
        elif tok.kind == "eof" and not expect_operand:
            while stack:
                if stack[-1].kind == "(":
                    raise ParseError("unbalanced '('", stack[-1].position)
                output.append(stack.pop().text)
        else:
            raise ParseError(f"unexpected {tok.text or 'end of input'!r}", tok.position)
    return output

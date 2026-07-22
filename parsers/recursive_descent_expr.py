"""Recursive descent: one function per grammar rule, building an AST.

The grammar encodes precedence in its shape rather than in a table. An
expression is a sum of terms, a term is a product of powers, and a factor is a
number, a name, a parenthesised expression, or a negated one. Because parse_expr
can only combine whole terms, multiplication has already been absorbed lower
down, so it binds tighter without any extra logic.

Associativity comes from the loop direction. Left-associative levels use a while
loop that folds each new operand onto the accumulated left node; power is
right-associative, so it recurses into itself on the right instead. Unary minus
also recurses into the power level, which is why -2 ** 2 parses as -(2 ** 2),
exactly as Python itself does.

The result is a tree, not a value, and that is the payoff: the same tree can be
evaluated, pretty-printed, optimised, or compiled. Parsing is O(n).
"""

from dataclasses import dataclass


class ParseError(Exception):
    def __init__(self, message: str, position: int) -> None:
        super().__init__(f"{message} (position {position})")
        self.position = position


@dataclass(frozen=True)
class Token:
    kind: str            # "num", "name", "op", "(", ")", "eof"
    text: str
    position: int


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    while i < len(source):
        ch = source[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit() or ch == ".":
            j = i
            while j < len(source) and (source[j].isdigit() or source[j] == "."):
                j += 1
            tokens.append(Token("num", source[i:j], i))
            i = j
        elif ch.isalpha() or ch == "_":
            j = i
            while j < len(source) and (source[j].isalnum() or source[j] == "_"):
                j += 1
            tokens.append(Token("name", source[i:j], i))
            i = j
        elif source[i:i + 2] == "**":
            tokens.append(Token("op", "**", i))
            i += 2
        elif ch in "+-*/%":
            tokens.append(Token("op", ch, i))
            i += 1
        elif ch in "()":
            tokens.append(Token(ch, ch, i))
            i += 1
        else:
            raise ParseError(f"unexpected character {ch!r}", i)
    tokens.append(Token("eof", "", len(source)))
    return tokens


@dataclass(frozen=True)
class Num:
    value: float


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Unary:
    op: str
    operand: "Node"


@dataclass(frozen=True)
class Binary:
    op: str
    left: "Node"
    right: "Node"


Node = Num | Var | Unary | Binary


class Parser:
    def __init__(self, source: str) -> None:
        self.tokens = tokenize(source)
        self.pos = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.pos]

    def accept(self, *texts: str) -> Token | None:
        token = self.current
        if token.kind == "op" and token.text in texts:
            self.pos += 1
            return token
        return None

    def parse(self) -> Node:
        node = self.parse_expr()
        if self.current.kind != "eof":
            raise ParseError(f"unexpected {self.current.text!r}",
                             self.current.position)
        return node

    def parse_expr(self) -> Node:
        node = self.parse_term()
        while op := self.accept("+", "-"):
            node = Binary(op.text, node, self.parse_term())
        return node

    def parse_term(self) -> Node:
        node = self.parse_power()
        while op := self.accept("*", "/", "%"):
            node = Binary(op.text, node, self.parse_power())
        return node

    def parse_power(self) -> Node:
        base = self.parse_factor()
        if op := self.accept("**"):
            # Recurse on the right so 2 ** 3 ** 2 groups as 2 ** (3 ** 2).
            return Binary(op.text, base, self.parse_power())
        return base

    def parse_factor(self) -> Node:
        if self.accept("-"):
            return Unary("-", self.parse_power())
        if self.accept("+"):
            return self.parse_power()
        token = self.current
        match token.kind:
            case "num":
                self.pos += 1
                return Num(float(token.text))
            case "name":
                self.pos += 1
                return Var(token.text)
            case "(":
                self.pos += 1
                node = self.parse_expr()
                if self.current.kind != ")":
                    raise ParseError("expected ')'", self.current.position)
                self.pos += 1
                return node
        raise ParseError(f"expected a value, found {token.text or 'end of input'!r}",
                         token.position)


def parse(source: str) -> Node:
    return Parser(source).parse()


def evaluate(node: Node, env: dict[str, float] | None = None) -> float:
    env = env or {}
    match node:
        case Num(value):
            return value
        case Var(name):
            if name not in env:
                raise ParseError(f"unbound name {name!r}", 0)
            return env[name]
        case Unary(_, operand):
            return -evaluate(operand, env)
        case Binary(op, left, right):
            a, b = evaluate(left, env), evaluate(right, env)
            match op:
                case "+":
                    return a + b
                case "-":
                    return a - b
                case "*":
                    return a * b
                case "/":
                    return a / b
                case "%":
                    return a % b
                case _:
                    return a ** b


def render(node: Node, indent: int = 0) -> str:
    pad = "  " * indent
    match node:
        case Num(value):
            return f"{pad}{value:g}"
        case Var(name):
            return f"{pad}{name}"
        case Unary(op, operand):
            return f"{pad}{op} (unary)\n{render(operand, indent + 1)}"
        case Binary(op, left, right):
            return (f"{pad}{op}\n{render(left, indent + 1)}\n"
                    f"{render(right, indent + 1)}")


def infix(node: Node) -> str:
    """Fully parenthesised, so the tree's grouping is visible at a glance."""
    match node:
        case Num(value):
            return f"{value:g}"
        case Var(name):
            return name
        case Unary(op, operand):
            return f"({op}{infix(operand)})"
        case Binary(op, left, right):
            return f"({infix(left)} {op} {infix(right)})"


def main() -> None:
    env = {"x": 4.0, "rate": 1.5}
    for source in [
        "1 + 2 * 3",
        "(1 + 2) * 3",
        "2 ** 3 ** 2",
        "10 - 4 - 3",
        "-2 ** 2",
        "-x + rate * 2",
        "-(x + 2) % 5",
    ]:
        tree = parse(source)
        print(f"{source:<14} => {infix(tree):<26} = {evaluate(tree, env):g}")

    print("\nAST for '-(x + 2) ** 2':")
    print(render(parse("-(x + 2) ** 2")))

    print()
    for bad in ["1 +", "(1 + 2", "2 3", "$", ""]:
        try:
            parse(bad)
        except ParseError as exc:
            print(f"{bad!r:<10} -> {exc}")

    try:
        evaluate(parse("y + 1"), env)
    except ParseError as exc:
        print(f"{'y + 1'!r:<10} -> {exc}")


if __name__ == "__main__":
    main()

"""A hand-written lexer: turn source text into typed tokens that carry positions.

A lexer is the first stage of every parser. It scans left to right and, at each
position, decides which single token starts there. The rule that keeps it simple
is maximal munch: consume the longest run that still forms a valid token, so
"12" is one number rather than two, and ">=" beats ">".

Positions are the part beginners skip and then regret. Recording the line and
column where each token started costs almost nothing during scanning and is the
only way to point at the offending character later; recovering it after the fact
is impossible once the text has been chopped up.

Anything the scanner cannot start a token with is an error raised immediately,
with the exact line and column, rather than a silently dropped character.
"""

from dataclasses import dataclass
from enum import Enum, auto


class Kind(Enum):
    NUMBER = auto()
    IDENT = auto()
    KEYWORD = auto()
    OP = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()


KEYWORDS = {"let", "if", "else", "true", "false"}
TWO_CHAR_OPS = {"==", "!=", "<=", ">=", "**"}
ONE_CHAR_OPS = set("+-*/%=<>")


@dataclass(frozen=True)
class Token:
    kind: Kind
    text: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.kind.name}({self.text!r}) at {self.line}:{self.column}"


class LexError(Exception):
    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(f"{message} at line {line}, column {column}")
        self.line, self.column = line, column


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    i, line, col = 0, 1, 1
    n = len(source)

    while i < n:
        ch = source[i]
        if ch == "\n":
            i, line, col = i + 1, line + 1, 1
            continue
        if ch in " \t\r":
            i, col = i + 1, col + 1
            continue
        if ch == "#":  # comment runs to end of line
            while i < n and source[i] != "\n":
                i += 1
            continue

        start_col = col
        if ch.isdigit():
            j = i
            seen_dot = False
            while j < n and (source[j].isdigit() or (source[j] == "." and not seen_dot)):
                seen_dot = seen_dot or source[j] == "."
                j += 1
            if source[j - 1] == ".":
                raise LexError("number ends in a dot", line, col + (j - 1 - i))
            tokens.append(Token(Kind.NUMBER, source[i:j], line, start_col))
        elif ch.isalpha() or ch == "_":
            j = i
            while j < n and (source[j].isalnum() or source[j] == "_"):
                j += 1
            word = source[i:j]
            kind = Kind.KEYWORD if word in KEYWORDS else Kind.IDENT
            tokens.append(Token(kind, word, line, start_col))
        elif source[i:i + 2] in TWO_CHAR_OPS:  # maximal munch before single ops
            j = i + 2
            tokens.append(Token(Kind.OP, source[i:j], line, start_col))
        elif ch in ONE_CHAR_OPS:
            j = i + 1
            tokens.append(Token(Kind.OP, ch, line, start_col))
        elif ch in "()":
            j = i + 1
            kind = Kind.LPAREN if ch == "(" else Kind.RPAREN
            tokens.append(Token(kind, ch, line, start_col))
        else:
            raise LexError(f"unexpected character {ch!r}", line, col)

        col += j - i
        i = j

    tokens.append(Token(Kind.EOF, "", line, col))
    return tokens


def main() -> None:
    source = "let rate = 1.5 * (base + 20) # trailing comment\nif rate >= 2 ** 3"
    for token in tokenize(source):
        print(token)

    print()
    for bad in ["let x = 4 $ 2", "value = 3.", "a\n  b ~ c"]:
        try:
            tokenize(bad)
        except LexError as exc:
            print(f"{bad!r} -> {exc}")

    print()
    print(f"empty source: {[str(t) for t in tokenize('')]}")
    print(f"only a comment: {[str(t) for t in tokenize('# nothing here')]}")


if __name__ == "__main__":
    main()

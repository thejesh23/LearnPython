"""Lexer: turn source text into tokens that remember where they started."""

from dataclasses import dataclass


class ParseError(ValueError):
    """A syntax error that remembers the character offset where it happened."""

    def __init__(self, message: str, position: int) -> None:
        super().__init__(f"{message} at position {position}")
        self.position = position


@dataclass(frozen=True)
class Token:
    """One lexeme: kind is "num", "name", "op", "(", ")" or "eof"."""

    kind: str
    text: str
    position: int


def tokenize(source: str) -> list[Token]:
    """Split ``source`` into tokens by maximal munch, ending with an "eof" token."""
    tokens, i = [], 0
    while i < len(source):
        ch, j = source[i], i + 1
        if ch.isspace():
            i = j
            continue
        if ch.isdigit() or ch == ".":
            seen_dot = ch == "."
            while j < len(source) and (source[j].isdigit() or (source[j] == "." and not seen_dot)):
                seen_dot = seen_dot or source[j] == "."
                j += 1
            if source[i:j] == ".":
                raise ParseError("a number needs a digit", i)
            kind = "num"
        elif ch.isalpha() or ch == "_":
            while j < len(source) and (source[j].isalnum() or source[j] == "_"):
                j += 1
            kind = "name"
        elif source.startswith("**", i):
            kind, j = "op", i + 2  # maximal munch: "**" beats "*"
        elif ch in "+-*/%":
            kind = "op"
        elif ch in "()":
            kind = ch
        else:
            raise ParseError(f"unexpected character {ch!r}", i)
        tokens.append(Token(kind, source[i:j], i))
        i = j
    tokens.append(Token("eof", "", len(source)))
    return tokens

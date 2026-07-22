"""A recursive-descent JSON parser, checked against the standard library.

JSON's grammar is small enough to parse straight from the character stream with
no separate lexer: the next non-space character alone decides which rule applies
('{' means object, '"' means string, '-' or a digit means number, and the three
literals are matched by name). Values nest, so parse_value calls itself through
parse_object and parse_array, and the recursion mirrors the data.

Two details do the real work. Strings need escape handling, including \\uXXXX
and the surrogate pairs that encode characters outside the basic plane. Numbers
must distinguish integers from floats, which JSON does by whether a fraction or
exponent is present, so "1" parses to int and "1.0" to float.

Errors carry the offset where parsing stopped. That is what makes a parser
usable: "expected ',' at position 17" beats a bare failure every time. Each
example below is compared against json.loads so correctness is demonstrated.
"""

import json
from typing import Any

WHITESPACE = " \t\n\r"
ESCAPES = {'"': '"', "\\": "\\", "/": "/", "b": "\b",
           "f": "\f", "n": "\n", "r": "\r", "t": "\t"}


class JSONParseError(ValueError):
    def __init__(self, message: str, position: int) -> None:
        super().__init__(f"{message} at position {position}")
        self.position = position


class Parser:
    def __init__(self, text: str) -> None:
        self.text = text
        self.i = 0

    def error(self, message: str) -> JSONParseError:
        return JSONParseError(message, self.i)

    def skip_space(self) -> None:
        while self.i < len(self.text) and self.text[self.i] in WHITESPACE:
            self.i += 1

    def peek(self) -> str:
        return self.text[self.i] if self.i < len(self.text) else ""

    def expect(self, ch: str) -> None:
        if self.peek() != ch:
            raise self.error(f"expected {ch!r}, found {self.peek() or 'end of input'!r}")
        self.i += 1

    def parse(self) -> Any:
        self.skip_space()
        value = self.parse_value()
        self.skip_space()
        if self.i != len(self.text):
            raise self.error("trailing data after the top-level value")
        return value

    def parse_value(self) -> Any:
        self.skip_space()
        ch = self.peek()
        if ch == "{":
            return self.parse_object()
        if ch == "[":
            return self.parse_array()
        if ch == '"':
            return self.parse_string()
        for word, value in (("true", True), ("false", False), ("null", None)):
            if self.text.startswith(word, self.i):
                self.i += len(word)
                return value
        if ch == "-" or ch.isdigit():
            return self.parse_number()
        raise self.error(f"unexpected {ch or 'end of input'!r}")

    def parse_object(self) -> dict[str, Any]:
        self.expect("{")
        obj: dict[str, Any] = {}
        self.skip_space()
        if self.peek() == "}":
            self.i += 1
            return obj
        while True:
            self.skip_space()
            if self.peek() != '"':
                raise self.error("object keys must be strings")
            key = self.parse_string()
            self.skip_space()
            self.expect(":")
            obj[key] = self.parse_value()
            self.skip_space()
            if self.peek() == ",":
                self.i += 1
                continue
            self.expect("}")
            return obj

    def parse_array(self) -> list[Any]:
        self.expect("[")
        items: list[Any] = []
        self.skip_space()
        if self.peek() == "]":
            self.i += 1
            return items
        while True:
            items.append(self.parse_value())
            self.skip_space()
            if self.peek() == ",":
                self.i += 1
                continue
            self.expect("]")
            return items

    def parse_string(self) -> str:
        self.expect('"')
        out: list[str] = []
        while True:
            if self.i >= len(self.text):
                raise self.error("unterminated string")
            ch = self.text[self.i]
            if ch == '"':
                self.i += 1
                return "".join(out)
            if ch == "\\":
                self.i += 1
                out.append(self.parse_escape())
                continue
            if ch < " ":
                raise self.error("raw control character in string")
            out.append(ch)
            self.i += 1

    def parse_escape(self) -> str:
        code = self.peek()
        if code in ESCAPES:
            self.i += 1
            return ESCAPES[code]
        if code != "u":
            raise self.error(f"unknown escape \\{code or 'end of input'}")
        value = self.read_hex4()
        # A high surrogate is only half a character; JSON encodes astral code
        # points as a surrogate pair, so pull in the partner when one follows.
        if 0xD800 <= value <= 0xDBFF and self.text[self.i:self.i + 2] == "\\u":
            mark = self.i
            self.i += 1
            low = self.read_hex4()
            if 0xDC00 <= low <= 0xDFFF:
                return chr(0x10000 + ((value - 0xD800) << 10) + (low - 0xDC00))
            self.i = mark  # not a valid pair; leave the second escape alone
        return chr(value)

    def read_hex4(self) -> int:
        self.i += 1  # skip the 'u'
        digits = self.text[self.i:self.i + 4]
        if len(digits) < 4 or any(d not in "0123456789abcdefABCDEF" for d in digits):
            raise self.error(f"bad unicode escape {digits!r}")
        self.i += 4
        return int(digits, 16)

    def parse_number(self) -> int | float:
        start = self.i
        if self.peek() == "-":
            self.i += 1
        self.read_digits(leading_zero_ok=False)
        is_float = False
        if self.peek() == ".":
            is_float = True
            self.i += 1
            self.read_digits()
        if self.peek() in ("e", "E"):
            is_float = True
            self.i += 1
            if self.peek() in ("+", "-"):
                self.i += 1
            self.read_digits()
        raw = self.text[start:self.i]
        return float(raw) if is_float else int(raw)

    def read_digits(self, leading_zero_ok: bool = True) -> None:
        start = self.i
        while self.peek().isdigit():
            self.i += 1
        if self.i == start:
            raise self.error("expected a digit")
        if not leading_zero_ok and self.text[start] == "0" and self.i - start > 1:
            raise JSONParseError("numbers may not have leading zeros", start)


def loads(text: str) -> Any:
    return Parser(text).parse()


def main() -> None:
    good = [
        "{}",
        "[]",
        '{"name": "ada", "age": 36, "tags": ["math", "engines"], "ok": true}',
        '[0, -1, 3.5, 1e3, -2.5E-2, null, false]',
        r'"escapes: \" \\ \/ \n \t é"',
        r'"surrogate pair: \ud83d\ude00, BMP: \u00e9"',
        '  {"nested": {"deep": [ {"x": [1, [2, [3]]]} ]}}  ',
    ]
    for text in good:
        mine, theirs = loads(text), json.loads(text)
        print(f"{text.strip()[:52]:<54} matches json: {mine == theirs}")
        if mine != theirs:
            print(f"  mine={mine!r} theirs={theirs!r}")

    print()
    bad = [
        '{"a": 1,}',
        "[1, 2",
        '{"a" 1}',
        "{'a': 1}",
        '"unterminated',
        "01",
        '"bad \\q escape"',
        "[1] extra",
        "",
    ]
    for text in bad:
        try:
            loads(text)
            print(f"{text!r:<20} -> NO ERROR (bug!)")
        except JSONParseError as exc:
            print(f"{text!r:<20} -> {exc}")

    print()
    # Types matter: JSON's grammar, not the value, decides int vs float.
    print(f"loads('1') -> {loads('1')!r}, loads('1.0') -> {loads('1.0')!r}")
    print(f"round-trip via json.dumps: "
          f"{loads(json.dumps({'a': [1, 2.5, None]})) == {'a': [1, 2.5, None]}}")


if __name__ == "__main__":
    main()

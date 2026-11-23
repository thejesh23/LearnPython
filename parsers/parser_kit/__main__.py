"""Examples and self-check: python3 -m parsers.parser_kit"""

import random
import sys
from typing import Any

from . import PATHS, ParseError, calculate, compile_tree, infix, parse, to_rpn, tokenize
from .backends import OPCODES, Instr
from .parser import number

ENV = {"x": 3, "rate": 1.5}


def examples() -> None:
    print("1. tokens:", [(t.kind, t.text) for t in tokenize("rate * (x + 2.5)")])
    print("2. trees show the grouping precedence chose:")
    for source in ("1 + 2 * 3", "10 - 4 - 3", "2 ** 3 ** 2", "-2 ** 2"):
        print(f"   {source:<11} => {infix(parse(source))}")
    print("3. postfix of '3 + 4 * (2 - x)':", " ".join(to_rpn("3 + 4 * (2 - x)")))
    print("4. bytecode of '2 + 3 * x':", "; ".join(map(str, compile_tree(parse("2 + 3 * x")))))
    print("5. tree, rpn and vm agree with Python:")
    for source in ("-x + rate * 2", "7 % 4 / 2", "2 ** -1"):
        values = {via: calculate(source, ENV, via) for via in PATHS}
        print(f"   {source:<14} {values}  python: {eval(source, {}, dict(ENV))}")
    print("6. errors point at the offending position:")
    for bad in ("1 +", "(1 + 2", "2 3", "4 $ 2"):
        try:
            parse(bad)
        except ParseError as exc:
            print(f"   {bad!r:<9} -> {exc}")


def outcome(func: Any, *args: Any) -> str:
    """repr of the result, or the exception type: compares 1 vs 1.0, nan, errors."""
    try:
        return repr(func(*args))
    except (ArithmeticError, NameError) as exc:
        return type(exc).__name__


def postfix_of(code: list[Instr]) -> list[str]:
    names = {name: sym for sym, name in OPCODES.items()} | {"NEG": "u-", "POS": "u+"}
    return [repr(i.arg) if i.op == "PUSH" else i.arg if i.op == "LOAD" else names[i.op] for i in code]


def check_agreement(source: str, env: dict[str, Any]) -> bool:
    """All parsers accept or reject together; accepted input evaluates like Python."""
    results = []
    for build in (parse, to_rpn):
        try:
            results.append(build(source))
        except ParseError:
            results.append(None)
    tree, rpn = results
    assert (tree is None) == (rpn is None), source
    if tree is None:
        return False
    # Same postfix from the tree compiler and from shunting-yard means the same tree.
    canonical = [repr(number(t)) if t[0].isdigit() or t[0] == "." else t for t in rpn]
    assert postfix_of(compile_tree(tree)) == canonical, (source, rpn)
    want = outcome(eval, compile(source, "<expr>", "eval"), {"__builtins__": {}}, env)
    for via in PATHS:
        assert outcome(calculate, source, env, via) == want, (source, via, want)
    return True


def random_expr(rng: random.Random, depth: int) -> str:
    if depth == 0 or rng.random() < 0.25:
        return rng.choice([str(rng.randint(0, 20)), f"{rng.randint(0, 9)}.{rng.randint(0, 9)}", "x", "rate"])
    roll = rng.random()
    if roll < 0.15:
        return rng.choice("-+") + random_expr(rng, depth - 1)
    if roll < 0.3:
        return f"({random_expr(rng, depth - 1)}) ** {rng.randint(0, 3)}"  # bounded powers
    op = rng.choice(["+", "-", "*", "/", "%", "+", "*"])
    return f"{random_expr(rng, depth - 1)} {op} {random_expr(rng, depth - 1)}"


def self_check() -> None:
    assert calculate("2 ** 3 ** 2") == 512 and calculate("-2 ** 2") == -4
    assert calculate("10 - 4 - 3") == 3 and calculate("7 / 2", via="rpn") == 3.5
    for bad in ("1 +", "(1 + 2", "1 + 2)", "2 3", "3 * / 4", "$", "", "()", "x (1)", "."):
        for build in (parse, to_rpn):
            try:
                build(bad)
            except ParseError:
                continue
            raise AssertionError(f"{build.__name__} accepted {bad!r}")
    try:
        calculate("y + 1", via="vm")
    except NameError:
        pass
    else:
        raise AssertionError("unbound name not reported")
    rng = random.Random(42)
    for _ in range(1500):
        assert check_agreement(random_expr(rng, 5), ENV)
    soup = ["1", "2", "x", "+", "-", "*", "/", "%", "**", "(", ")"]
    accepted = 0
    for _ in range(4000):  # random token soup: x=2 keeps power towers small
        accepted += check_agreement(" ".join(rng.choices(soup, k=rng.randint(1, 9))), {"x": 2})
    assert accepted > 100, accepted


def main() -> int:
    examples()
    self_check()
    print("self-check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

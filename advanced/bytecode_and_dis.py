"""Reading CPython bytecode with `dis` — what your code actually does.

Python compiles source to bytecode for a stack machine, then the interpreter
loop executes it. `dis.dis` shows those instructions, which settles arguments
that benchmarks only hint at: why `+=` on a list differs from `+`, why a local
variable beats a global, what a comprehension really compiles to.

Bytecode is a CPython implementation detail and changes between versions. Read
it to understand, never to depend on.
"""

import dis


def add_locals(a, b):
    return a + b


GLOBAL_VALUE = 10


def read_global():
    return GLOBAL_VALUE


def read_local():
    value = 10
    return value


def with_comprehension(items):
    return [x * 2 for x in items]


def with_loop(items):
    out = []
    for x in items:
        out.append(x * 2)
    return out


def main() -> None:
    print("add_locals:")
    dis.dis(add_locals)

    print("\nglobal lookup (LOAD_GLOBAL: a dict lookup at runtime):")
    dis.dis(read_global)

    print("\nlocal lookup (LOAD_FAST: an array index):")
    dis.dis(read_local)

    print("\nconstant folding — the compiler evaluates this at compile time:")
    dis.dis(compile("x = 2 * 60 * 60", "<demo>", "exec"))

    print("\ncomprehension instruction count vs explicit loop:")
    comp = list(dis.get_instructions(with_comprehension))
    loop = list(dis.get_instructions(with_loop))
    print(f"  comprehension: {len(comp)} instructions")
    print(f"  explicit loop: {len(loop)} instructions")

    print("\ncode object internals:")
    code = with_loop.__code__
    print(f"  co_varnames = {code.co_varnames}")
    print(f"  co_consts   = {code.co_consts}")
    print(f"  co_names    = {code.co_names}")
    print(f"  stack size  = {code.co_stacksize}")


if __name__ == "__main__":
    main()

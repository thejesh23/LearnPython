# parser_kit

An arithmetic pipeline (lexer, two parsers, three evaluators) that follows Python's precedence rules, checked against Python's own `eval`.

```bash
python3 -m parsers.parser_kit     # six examples plus a randomized self-check (from the repo root)
```

```python
from parsers.parser_kit import calculate, parse, infix, to_rpn

calculate("2 ** 3 ** 2 - x", {"x": 12}, via="vm")   # 500
infix(parse("-2 ** 2"))                              # '(-(2 ** 2))'
to_rpn("3 + 4 * 2")                                  # ['3', '4', '2', '*', '+']
```

| API | Module | Stage |
|---|---|---|
| `tokenize`, `Token`, `ParseError` | `lexer.py` | text to tokens with positions |
| `parse` (recursive descent), `to_rpn` (shunting-yard) | `parser.py` | tokens to a tree or to postfix |
| `evaluate`, `eval_rpn`, `compile_tree` + `run` | `backends.py` | tree walk, postfix stack, bytecode on a stack VM |
| `calculate(source, env, via)` | `__init__.py` | one call, `via` = `"tree"`, `"rpn"` or `"vm"` |

The self-check proves the two parsers build the same tree: the compiled bytecode and the shunting-yard output are the same postfix sequence.
Standalone versions live next to this folder, e.g. `../shunting_yard.py` and `../stack_vm.py`.

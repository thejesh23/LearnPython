# 15 · Typing

Type hints beyond the basics: generics, TypedDict, overloads and runtime hints.

Read the files in this order; each one runs on its own:

| # | File | What it teaches |
|---|------|-----------------|
| 1 | [`generics.py`](generics.py) | Generics — code that works for many types without forgetting which type it got. |
| 2 | [`typed_dict_and_literal.py`](typed_dict_and_literal.py) | `TypedDict` and `Literal` — describing JSON-like data with types. |
| 3 | [`callables_and_overloads.py`](callables_and_overloads.py) | Typing callables: `Callable`, `ParamSpec` for decorators, and `@overload`. |
| 4 | [`aliases_newtype_final.py`](aliases_newtype_final.py) | Naming and pinning down types: `type`, `NewType`, `Final`, `ClassVar`, `Self`. |
| 5 | [`hints_at_runtime.py`](hints_at_runtime.py) | What happens to type hints when the program actually runs. |

```bash
python3 basics/15_typing/generics.py
```

## Practice

Open [`exercises/ch15_typing.py`](../../exercises/ch15_typing.py), fill in each function, and run the file until every line says `[solved]`. Stuck? Compare with [`exercises/solutions/ch15_typing.py`](../../exercises/solutions/ch15_typing.py).

## Going deeper

- [`advanced/typing_generics.py`](../../advanced/typing_generics.py)

---

← [14_testing](../14_testing/) · [16_threads_and_processes](../16_threads_and_processes/) →

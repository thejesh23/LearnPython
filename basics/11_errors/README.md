# 11 · Errors

Handling, raising and designing exceptions, warnings, and debugging.

Read the files in this order; each one runs on its own:

| # | File | What it teaches |
|---|------|-----------------|
| 1 | [`try_except.py`](try_except.py) | `try` / `except` / `else` / `finally` — handling what goes wrong. |
| 2 | [`raising_exceptions.py`](raising_exceptions.py) | Raising — failing loudly, and keeping the cause. |
| 3 | [`custom_exceptions.py`](custom_exceptions.py) | Custom exception hierarchies — and the modern extras. |
| 4 | [`exception_groups.py`](exception_groups.py) | Exception groups, `except*`, and notes on exceptions (Python 3.11+). |
| 5 | [`warnings_module.py`](warnings_module.py) | `warnings` — telling the caller "this works, but you should change it". |
| 6 | [`debugging_tools.py`](debugging_tools.py) | Debugging tools — reading tracebacks, inspecting the stack, and `breakpoint()`. |

```bash
python3 basics/11_errors/try_except.py
```

## Practice

Open [`exercises/ch11_errors.py`](../../exercises/ch11_errors.py), fill in each function, and run the file until every line says `[solved]`. Stuck? Compare with [`exercises/solutions/ch11_errors.py`](../../exercises/solutions/ch11_errors.py).

## Going deeper

- [`advanced/exception_chaining.py`](../../advanced/exception_chaining.py)

---

← [10_async](../10_async/) · [12_modules_io](../12_modules_io/) →

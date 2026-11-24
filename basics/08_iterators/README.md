# 08 · Iterators and generators

What `for` really does, `yield`, lazy pipelines and itertools.

Read the files in this order; each one runs on its own:

| # | File | What it teaches |
|---|------|-----------------|
| 1 | [`iterables_and_iterators.py`](iterables_and_iterators.py) | The iterator protocol — what `for` actually does. |
| 2 | [`generators.py`](generators.py) | `yield` — writing an iterator as an ordinary function. |
| 3 | [`itertools_tour.py`](itertools_tour.py) | `itertools` — the standard library's iterator toolkit. |
| 4 | [`generator_pipelines.py`](generator_pipelines.py) | Generator pipelines: chaining lazy steps so data flows one item at a time. |
| 5 | [`yield_from_and_send.py`](yield_from_and_send.py) | `yield from`, generator return values, `send()` and `close()`. |

```bash
python3 basics/08_iterators/iterables_and_iterators.py
```

## Practice

Open [`exercises/ch08_iterators.py`](../../exercises/ch08_iterators.py), fill in each function, and run the file until every line says `[solved]`. Stuck? Compare with [`exercises/solutions/ch08_iterators.py`](../../exercises/solutions/ch08_iterators.py).

## Going deeper

- [`advanced/generators_as_coroutines.py`](../../advanced/generators_as_coroutines.py)
- [`advanced/lazy_evaluation_pipelines.py`](../../advanced/lazy_evaluation_pipelines.py)

---

← [07_collections](../07_collections/) · [09_classes](../09_classes/) →

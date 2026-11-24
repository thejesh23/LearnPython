# 20 · Performance

Measuring before optimising: timeit, profiling, memory, and data-structure choices.

Read the files in this order; each one runs on its own:

| # | File | What it teaches |
|---|------|-----------------|
| 1 | [`measuring_with_timeit.py`](measuring_with_timeit.py) | Measuring speed: `time.perf_counter` and the `timeit` module. |
| 2 | [`profiling_with_cprofile.py`](profiling_with_cprofile.py) | Profiling with `cProfile` and `pstats`: find out *where* the time goes. |
| 3 | [`memory_with_tracemalloc.py`](memory_with_tracemalloc.py) | Measuring memory: `sys.getsizeof` versus `tracemalloc`. |
| 4 | [`choosing_data_structures.py`](choosing_data_structures.py) | Choosing the right data structure — usually the biggest speed-up available. |
| 5 | [`faster_python_idioms.py`](faster_python_idioms.py) | Faster Python idioms — and the habit of measuring before believing them. |

```bash
python3 basics/20_performance/measuring_with_timeit.py
```

## Practice

Open [`exercises/ch20_performance.py`](../../exercises/ch20_performance.py), fill in each function, and run the file until every line says `[solved]`. Stuck? Compare with [`exercises/solutions/ch20_performance.py`](../../exercises/solutions/ch20_performance.py).

## Going deeper

- [`advanced/profiling_and_benchmarking.py`](../../advanced/profiling_and_benchmarking.py)
- [`advanced/bytecode_and_dis.py`](../../advanced/bytecode_and_dis.py)

---

← [19_networking](../19_networking/) · [21_pythonic_code](../21_pythonic_code/) →

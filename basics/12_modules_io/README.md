# 12 · Modules and I/O

Imports, files, JSON, CSV, config files and `with` blocks.

Read the files in this order; each one runs on its own:

| # | File | What it teaches |
|---|------|-----------------|
| 1 | [`modules_and_imports.py`](modules_and_imports.py) | Modules, packages, and imports. |
| 2 | [`files_and_pathlib.py`](files_and_pathlib.py) | Reading and writing files with `pathlib`. |
| 3 | [`context_managers.py`](context_managers.py) | `with` — guaranteed cleanup, even when something raises. |
| 4 | [`contextlib_tools.py`](contextlib_tools.py) | `contextlib` — ready-made context managers for everyday jobs. |
| 5 | [`json_io.py`](json_io.py) | JSON — `dumps`/`loads` for strings, `dump`/`load` for files. |
| 6 | [`csv_io.py`](csv_io.py) | Reading and writing CSV files with the `csv` module. |
| 7 | [`config_files.py`](config_files.py) | Configuration — TOML, INI files, environment variables, and layering them. |

```bash
python3 basics/12_modules_io/modules_and_imports.py
```

## Practice

Open [`exercises/ch12_modules_io.py`](../../exercises/ch12_modules_io.py), fill in each function, and run the file until every line says `[solved]`. Stuck? Compare with [`exercises/solutions/ch12_modules_io.py`](../../exercises/solutions/ch12_modules_io.py).

## Going deeper

- [`advanced/dynamic_imports.py`](../../advanced/dynamic_imports.py)
- [`advanced/csv_data_processing.py`](../../advanced/csv_data_processing.py)
- [`parsers/`](../../parsers/)

---

← [11_errors](../11_errors/) · [13_standard_library](../13_standard_library/) →

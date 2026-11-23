# toolbox_kit

Six reusable utilities built from the language features the `advanced/` samples teach: decorators, `functools`, generators, descriptors, dataclasses and exception chaining.

```bash
python3 -m advanced.toolbox_kit     # seven examples plus a self-check
```

| API | Module | Built on |
|---|---|---|
| `timed` | `functions.py` | `functools.wraps`, `time.perf_counter` |
| `retry`, `RetryError` | `functions.py` | a decorator factory, `raise ... from` |
| `describe` | `functions.py` | `functools.singledispatch` |
| `Pipeline` | `functions.py` | lazy generators, `itertools.islice` / `batched` |
| `Field` | `objects.py` | a data descriptor with `__set_name__` |
| `load_config`, `ConfigError` | `objects.py` | `dataclasses.fields`, `typing.get_type_hints` |

Standalone versions live next to this folder, e.g. `../descriptors.py` and `../functools_toolkit.py`.

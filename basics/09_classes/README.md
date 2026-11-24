# 09 · Classes

Bundling data and behaviour: from a first class to descriptors and metaclasses.

Read the files in this order; each one runs on its own:

| # | File | What it teaches |
|---|------|-----------------|
| 1 | [`basic_class.py`](basic_class.py) | Classes — bundling data with the functions that operate on it. |
| 2 | [`properties.py`](properties.py) | `@property` — a method that is read like an attribute. |
| 3 | [`class_and_static_methods.py`](class_and_static_methods.py) | Instance methods, `@classmethod` and `@staticmethod`. |
| 4 | [`dunder_methods.py`](dunder_methods.py) | Dunder methods — how your class plugs into Python's syntax. |
| 5 | [`dataclasses_intro.py`](dataclasses_intro.py) | `@dataclass` — the boilerplate remover for classes that mostly hold data. |
| 6 | [`enums.py`](enums.py) | `Enum` — a fixed set of named constants, checkable and self-documenting. |
| 7 | [`inheritance.py`](inheritance.py) | Inheritance, `super()`, and why Python rarely needs it. |
| 8 | [`composition_over_inheritance.py`](composition_over_inheritance.py) | Composition over inheritance — build objects from parts instead of parents. |
| 9 | [`abstract_and_protocols.py`](abstract_and_protocols.py) | Two ways to describe an interface: ABCs and Protocols. |
| 10 | [`equality_and_hashing.py`](equality_and_hashing.py) | `__eq__` and `__hash__` — the contract behind dict keys and set members. |
| 11 | [`slots.py`](slots.py) | `__slots__` — fixed attributes, smaller objects. |
| 12 | [`descriptors.py`](descriptors.py) | Descriptors — the machinery under `property`, methods and `classmethod`. |
| 13 | [`init_subclass_and_metaclasses.py`](init_subclass_and_metaclasses.py) | Customising class creation: class decorators, `__init_subclass__`, metaclasses. |

```bash
python3 basics/09_classes/basic_class.py
```

## Practice

Open [`exercises/ch09_classes.py`](../../exercises/ch09_classes.py), fill in each function, and run the file until every line says `[solved]`. Stuck? Compare with [`exercises/solutions/ch09_classes.py`](../../exercises/solutions/ch09_classes.py).

## Going deeper

- [`advanced/dataclass_patterns.py`](../../advanced/dataclass_patterns.py)
- [`advanced/descriptors.py`](../../advanced/descriptors.py)
- [`advanced/metaclasses.py`](../../advanced/metaclasses.py)
- [`advanced/slots_and_memory.py`](../../advanced/slots_and_memory.py)
- [`advanced/class_decorators_and_mixins.py`](../../advanced/class_decorators_and_mixins.py)
- [`advanced/enum_state_machines.py`](../../advanced/enum_state_machines.py)
- [`advanced/introspection_and_reflection.py`](../../advanced/introspection_and_reflection.py)
- [`advanced/weakrefs_and_gc.py`](../../advanced/weakrefs_and_gc.py)

---

← [08_iterators](../08_iterators/) · [10_async](../10_async/) →

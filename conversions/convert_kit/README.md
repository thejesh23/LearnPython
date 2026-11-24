# convert_kit

The `conversions/` samples behind one small API: unit conversion through a
base unit, Roman numerals, English number words and any base from 2 to 36.

```bash
python3 -m conversions.convert_kit     # seven examples plus a self-check
```

| Function | Module | What it does |
|---|---|---|
| `convert(value, source, target)` | `units.py` | temperature, data sizes, time and length, through one base unit per quantity |
| `humanize_bytes(n, si=False)`, `clock(seconds)` | `units.py` | display helpers for sizes and durations |
| `to_roman(n)`, `from_roman(text)` | `numerals.py` | canonical Roman numerals, strict parsing |
| `to_words(n)` | `numerals.py` | British-style English number names |
| `to_base(n, base)`, `from_base(text, base)` | `numerals.py` | positional notation in bases 2..36 |

Adding a unit is one line in `UNITS`. Standalone versions live next to this
folder, e.g. `../temperature_conversions.py`.

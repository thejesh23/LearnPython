# string_kit

One `find_all()` over naive, KMP, Z, Rabin-Karp and suffix-array search, plus Aho-Corasick and a handful of classic string utilities.

```bash
python3 -m strings.string_kit     # eight examples plus a randomized self-check (from the repo root)
```

```python
from strings.string_kit import find_all, find_many, longest_palindrome

find_all("abababa", "aba", algo="z")              # [0, 2, 4]  (overlaps count)
find_many("ushers", ["he", "she", "hers"])         # {'he': [2], 'she': [1], 'hers': [2]}
longest_palindrome("forgeeksskeegfor")             # 'geeksskeeg'
```

| API | Module |
|---|---|
| `find_all(text, pattern, algo)`, `ALGORITHMS` | `__init__.py` |
| `naive_search`, `kmp_search` + `build_lps`, `z_search` + `z_array`, `rabin_karp`, `suffix_array_search` + `suffix_array` | `search.py` |
| `find_many` (Aho-Corasick), `longest_palindrome` (Manacher), `longest_repeated_substring` (suffix array + LCP), `longest_unique_substring` (sliding window), `rle_encode` / `rle_decode`, `glob_match` | `text.py` |

Every search algorithm is checked against `str.startswith` at each position, and `glob_match` against `fnmatch.fnmatchcase`.
Standalone versions live next to this folder, e.g. `../kmp_search.py` and `../manacher.py`.

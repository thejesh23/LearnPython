# 18 · Data and storage

SQLite, pickle, binary data, archives, hashing and secrets.

Read the files in this order; each one runs on its own:

| # | File | What it teaches |
|---|------|-----------------|
| 1 | [`sqlite3_basics.py`](sqlite3_basics.py) | `sqlite3` — a real SQL database that ships with Python. |
| 2 | [`sqlite3_queries.py`](sqlite3_queries.py) | More SQL with `sqlite3`: executemany, joins, GROUP BY and transactions. |
| 3 | [`pickle_and_its_dangers.py`](pickle_and_its_dangers.py) | `pickle` — save almost any Python object, and why never to load a stranger's. |
| 4 | [`binary_data_and_struct.py`](binary_data_and_struct.py) | Binary data: `bytes`, `bytearray`, byte order and the `struct` module. |
| 5 | [`compression_and_archives.py`](compression_and_archives.py) | Compressing data and bundling files: `gzip`, `zipfile`, `tarfile`, `shutil`. |
| 6 | [`hashing_and_secrets.py`](hashing_and_secrets.py) | Hashes, message signatures, random tokens and password storage. |

```bash
python3 basics/18_data_and_storage/sqlite3_basics.py
```

## Practice

Open [`exercises/ch18_data_and_storage.py`](../../exercises/ch18_data_and_storage.py), fill in each function, and run the file until every line says `[solved]`. Stuck? Compare with [`exercises/solutions/ch18_data_and_storage.py`](../../exercises/solutions/ch18_data_and_storage.py).

## Going deeper

- [`advanced/sqlite_basics.py`](../../advanced/sqlite_basics.py)
- [`advanced/pickle_and_serialisation.py`](../../advanced/pickle_and_serialisation.py)
- [`advanced/hashing_and_secrets.py`](../../advanced/hashing_and_secrets.py)
- [`advanced/memoryview_and_buffers.py`](../../advanced/memoryview_and_buffers.py)
- [`compression/`](../../compression/)
- [`crypto/`](../../crypto/)

---

← [17_os_and_command_line](../17_os_and_command_line/) · [19_networking](../19_networking/) →

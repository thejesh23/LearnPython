# 19 · Networking

URLs, sockets, HTTP servers and clients, and talking to JSON APIs.

Read the files in this order; each one runs on its own:

| # | File | What it teaches |
|---|------|-----------------|
| 1 | [`urls_and_query_strings.py`](urls_and_query_strings.py) | `urllib.parse` — take URLs apart, build them safely, and resolve links. |
| 2 | [`sockets_echo_server.py`](sockets_echo_server.py) | TCP sockets — a tiny echo server and client talking over 127.0.0.1. |
| 3 | [`http_server_and_client.py`](http_server_and_client.py) | HTTP with only the standard library: `http.server` and `urllib.request`. |
| 4 | [`json_api_client.py`](json_api_client.py) | A small JSON API client: timeouts, error handling and retries with backoff. |

```bash
python3 basics/19_networking/urls_and_query_strings.py
```

## Practice

Open [`exercises/ch19_networking.py`](../../exercises/ch19_networking.py), fill in each function, and run the file until every line says `[solved]`. Stuck? Compare with [`exercises/solutions/ch19_networking.py`](../../exercises/solutions/ch19_networking.py).

## Going deeper

- [`distributed/`](../../distributed/)

---

← [18_data_and_storage](../18_data_and_storage/) · [20_performance](../20_performance/) →

"""Practice: networking (chapter 19).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch19_networking.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

Nothing here needs the internet: the tests start their own small servers on
127.0.0.1 (this machine only) and stop them again.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch19_networking.py: try first, peek second. The lessons
for this chapter are in basics/19_networking/.
"""

from collections.abc import Callable
from typing import Any


def verdict(error: BaseException) -> str:
    """Turn the exception a test raised into a short status."""
    # A stub raises NotImplementedError. Other errors may wrap it, so follow
    # the chain of causes (and look inside exception groups) before deciding.
    link: BaseException | None = error
    for _ in range(20):
        if link is None:
            break
        if isinstance(link, NotImplementedError):
            return "[todo] not attempted"
        if isinstance(link, BaseExceptionGroup) and link.subgroup(
            NotImplementedError
        ):
            return "[todo] not attempted"
        link = link.__cause__ or link.__context__
    if isinstance(error, AssertionError):
        return f"[not yet] {str(error) or 'a check failed'}"
    return f"[not yet] {type(error).__name__}: {error}"


def report(title: str, test: Callable[[Any], None], impl: Any) -> None:
    """Run one test against one implementation and print a one-line status."""
    try:
        test(impl)
        status = "[solved]"
    except KeyboardInterrupt:
        raise
    except BaseException as error:  # never crash: one line per exercise
        status = verdict(error)
    print(f"{title:<40} {status}")


# --- Exercise 1 -------------------------------------------------------------

def get_param(url: str, name: str) -> str | None:
    """Return the value of query parameter `name` in `url`, decoded.

        url = "https://shop.example/search?q=caf%C3%A9+au+lait&page=2#top"
        get_param(url, "q")     ->  "café au lait"
        get_param(url, "page")  ->  "2"
        get_param(url, "top")   ->  None    (the fragment is not the query)

    If the name appears more than once, return the first value. A parameter
    that is present but empty ("?q=&page=1") gives "", not None. Use
    urllib.parse: urlsplit for the query part, then parse_qs (look up its
    keep_blank_values option).
    """
    raise NotImplementedError


def test_get_param(impl: Callable[[str, str], str | None]) -> None:
    url = "https://shop.example/search?q=caf%C3%A9+au+lait&page=2#top"
    cases = [
        (url, "q", "café au lait"),
        (url, "page", "2"),
        (url, "top", None),
        (url, "missing", None),
        ("https://x.example/?tag=red&tag=blue", "tag", "red"),
        ("https://x.example/?q=&page=1", "q", ""),
        ("https://x.example/?sum=1%2B1%3D2", "sum", "1+1=2"),
        ("https://x.example/no/query", "q", None),
    ]
    for address, name, want in cases:
        got = impl(address, name)
        assert got == want, (
            f"get_param({address!r}, {name!r}) gave {got!r}, not {want!r}"
        )


def check_get_param() -> None:
    report("1. get_param", test_get_param, get_param)


# --- Exercise 2 -------------------------------------------------------------

def add_params(url: str, params: dict[str, str | int]) -> str:
    """Return `url` with `params` added to its query string.

    - Parameters already in the URL keep their place; a name given in
      params replaces the old value in that same place.
    - New names go at the end, in the order of params.
    - Values are encoded properly ("fish & chips" -> "fish+%26+chips").
    - The fragment (#...) and everything else stays as it was.

        url = "https://x.example/s?q=old&page=1#top"
        add_params(url, {"page": 3, "lang": "en"})
        ->  "https://x.example/s?q=old&page=3&lang=en#top"

    Split with urlsplit, read the old query with parse_qsl into a dict,
    update it, build the new query with urlencode, put it back with
    ._replace(query=...) and urlunsplit.
    """
    raise NotImplementedError


def test_add_params(impl: Callable[[str, dict[str, str | int]], str]) -> None:
    cases = [
        ("https://x.example/s?q=old&page=1#top", {"page": 3, "lang": "en"},
         "https://x.example/s?q=old&page=3&lang=en#top"),
        ("https://x.example/s", {"q": "fish & chips"},
         "https://x.example/s?q=fish+%26+chips"),
        ("https://x.example/s?a=1", {}, "https://x.example/s?a=1"),
        ("http://127.0.0.1:8000/api?empty=", {"n": 1},
         "http://127.0.0.1:8000/api?empty=&n=1"),
        ("https://x.example/s", {"city": "Zürich"},
         "https://x.example/s?city=Z%C3%BCrich"),
    ]
    for url, params, want in cases:
        got = impl(url, params)
        assert got == want, (
            f"add_params({url!r}, {params}) gave {got!r}, not {want!r}"
        )


def check_add_params() -> None:
    report("2. add_params", test_add_params, add_params)


def main() -> None:
    check_get_param()
    check_add_params()


if __name__ == "__main__":
    main()

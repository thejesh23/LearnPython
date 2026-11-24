"""`urllib.parse` — take URLs apart, build them safely, and resolve links.

A URL looks like one string but it is really a small record:

    https://user@shop.example:8443/search/books?q=python&page=2#results
    scheme   netloc                path         query             fragment

Gluing URLs together with `+` and f-strings goes wrong as soon as a value
contains a space, an `&` or a non-ASCII letter. `urllib.parse` does the fiddly
parts for you:

    urlsplit / urlunsplit   URL string <-> named parts
    quote / unquote         percent-encode one piece ("a b" -> "a%20b")
    urlencode / parse_qs    dict of parameters <-> "a=1&b=2" query string
    urljoin                 resolve a relative link against a base URL

Nothing in this file touches the network: it is all string processing.
"""

from urllib.parse import urlsplit
from urllib.parse import urlunsplit


def split_demo() -> None:
    url = "https://user@shop.example:8443/search/books?q=python&page=2#results"
    parts = urlsplit(url)
    # The result is a named tuple: read fields by name, not by index.
    for field in ("scheme", "netloc", "path", "query", "fragment"):
        print(f"{field:>8}: {getattr(parts, field)!r}")
    # netloc is further split into handy attributes.
    print(f"hostname={parts.hostname!r} port={parts.port} user={parts.username!r}")

    # Named tuples are immutable; _replace returns a changed copy.
    public = parts._replace(netloc="shop.example", fragment="")
    print(f"rebuilt without user, port, fragment: {urlunsplit(public)}")

    # A URL with no scheme is read as a path, which surprises people.
    print(f"no scheme: {urlsplit('shop.example/books')}")


def main() -> None:
    split_demo()


if __name__ == "__main__":
    main()

"""Async context managers — `async with` and the tools in `contextlib`.

`async with` is `with` for resources whose setup or teardown has to await: a
network connection, a database transaction, a lock. Writing `__aenter__` and
`__aexit__` by hand is shown in async_generators.py; this file covers the
shortcuts:

    @asynccontextmanager  write setup / yield / teardown as one async function
    AsyncExitStack        enter a number of async context managers that is
                          only known at runtime, and exit them all safely
    aclosing              make sure an async generator's cleanup runs as
                          soon as you stop iterating it, not "eventually"
"""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


class Connection:
    def __init__(self, host: str) -> None:
        self.host = host
        self.open = False

    async def query(self, sql: str) -> str:
        await asyncio.sleep(0)
        if "drop" in sql:
            raise PermissionError("not allowed")
        return f"{self.host}: rows for {sql!r}"


@asynccontextmanager
async def connect(host: str) -> AsyncIterator[Connection]:
    conn = Connection(host)
    await asyncio.sleep(0)  # pretend handshake
    conn.open = True
    print(f"  opened {host}")
    try:
        yield conn  # the body of `async with` runs here
    finally:  # runs even when the body raises
        await asyncio.sleep(0)  # pretend goodbye message
        conn.open = False
        print(f"  closed {host}")


async def asynccontextmanager_main() -> None:
    print("@asynccontextmanager, normal exit and exit by exception:")
    async with connect("db1") as conn:
        print(f"  {await conn.query('select 1')}")

    try:
        async with connect("db2") as conn:
            await conn.query("drop table users")
    except PermissionError as exc:
        print(f"  PermissionError: {exc}; still open? {conn.open}")


def asynccontextmanager_demo() -> None:
    asyncio.run(asynccontextmanager_main())


def main() -> None:
    asynccontextmanager_demo()


if __name__ == "__main__":
    main()

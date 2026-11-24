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
from contextlib import AsyncExitStack
from contextlib import aclosing
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


async def query_all(hosts: list[str]) -> list[str]:
    # One `async with` per host cannot be written when the list length is
    # only known at runtime. The stack collects them and closes them all,
    # in reverse order, when its own block ends.
    async with AsyncExitStack() as stack:
        conns = [await stack.enter_async_context(connect(h)) for h in hosts]
        return [await c.query("select 1") for c in conns]


async def exit_stack_main() -> None:
    print("AsyncExitStack over three hosts:")
    results = await query_all(["east", "west", "north"])
    print(f"  got {len(results)} results")

    # If opening the third resource fails, the first two are still closed.
    print("AsyncExitStack with a failure partway through:")
    try:
        async with AsyncExitStack() as stack:
            for host in ["a", "b", "broken"]:
                if host == "broken":
                    raise ConnectionError(f"cannot reach {host}")
                await stack.enter_async_context(connect(host))
    except ConnectionError as exc:
        print(f"  ConnectionError: {exc}")


def exit_stack_demo() -> None:
    asyncio.run(exit_stack_main())


async def read_rows(log: list[str]) -> AsyncIterator[int]:
    log.append("open cursor")
    try:
        for n in range(100):
            await asyncio.sleep(0)
            yield n
    finally:
        log.append("close cursor")


async def aclosing_main() -> None:
    print("stopping an async generator early:")
    log: list[str] = []
    rows = read_rows(log)
    async for n in rows:
        if n == 2:
            break  # stop early: the generator is paused, not finished
    print(f"  after break:     {log}")
    # Its finally block runs only when the generator is closed: explicitly,
    # or whenever the garbage collector and event loop get round to it.
    await rows.aclose()
    print(f"  after aclose():  {log}")

    log.clear()
    async with aclosing(read_rows(log)) as rows:
        async for n in rows:
            if n == 2:
                break
    print(f"  with aclosing(): {log}")


def aclosing_demo() -> None:
    asyncio.run(aclosing_main())


def main() -> None:
    asynccontextmanager_demo()
    print()
    exit_stack_demo()
    print()
    aclosing_demo()


if __name__ == "__main__":
    main()

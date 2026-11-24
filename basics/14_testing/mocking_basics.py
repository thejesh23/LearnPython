"""`unittest.mock` — stand-ins for things a test should not really touch.

Code that sends email, calls a web API or reads the clock is hard to test:
the real thing is slow, costs money, or gives a different answer each time. A
Mock is an object that accepts any call, returns whatever you tell it to, and
remembers how it was called so the test can check.

    Mock()          an object that records every call
    return_value    what calling it returns
    side_effect     raise an error, or return a different value per call
    patch(...)      temporarily replace a real name while a test runs

Mock the boundary (the network, the clock), not your own logic.
"""

from unittest.mock import Mock


def notify_all(users: list[str], sender) -> int:
    for user in users:
        sender.send(to=user, text="Your order has shipped")
    return len(users)


def recording_demo() -> None:
    # Pass a Mock where the real email sender would go.
    sender = Mock()
    count = notify_all(["ana", "bo"], sender)
    print(f"notified {count} users")
    print(f"send called {sender.send.call_count} times")
    print(f"last call: {sender.send.call_args}")
    # assert_called_with raises AssertionError if the call did not happen.
    sender.send.assert_called_with(to="bo", text="Your order has shipped")
    print("assert_called_with passed")


def fetch_with_retry(fetch, attempts: int = 3) -> str:
    for attempt in range(1, attempts + 1):
        try:
            return fetch()
        except ConnectionError:
            print(f"  attempt {attempt} failed")
    raise ConnectionError("gave up")


def return_and_side_effect_demo() -> None:
    always_ok = Mock(return_value="<html>")
    print(f"result: {fetch_with_retry(always_ok)}")

    # A list as side_effect gives one outcome per call; exceptions are raised.
    flaky = Mock(side_effect=[ConnectionError(), ConnectionError(), "<html>"])
    print(f"result after retries: {fetch_with_retry(flaky)}")

    down = Mock(side_effect=ConnectionError())
    try:
        fetch_with_retry(down)
    except ConnectionError as exc:
        print(f"finally: {exc}")


def main() -> None:
    recording_demo()
    print()
    return_and_side_effect_demo()


if __name__ == "__main__":
    main()

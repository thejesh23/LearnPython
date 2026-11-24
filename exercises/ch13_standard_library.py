"""Practice: the standard library (chapter 13).

How to work through this file:
  1. Read an exercise's docstring, then replace each `raise NotImplementedError`
     line in it with your own code.
  2. Run the file:  python exercises/ch13_standard_library.py
  3. Every exercise prints one line:
         [solved]                 all checks passed
         [not yet] <message>      a check failed; the message says which one
         [todo] not attempted     the stub still raises NotImplementedError
  4. Aim for all [solved]. The test_... function under each exercise shows
     exactly what is checked; read it when a message is unclear, but do not
     edit it.

The exercises go from easy to a bit challenging. Stuck? Worked solutions are
in exercises/solutions/ch13_standard_library.py: try first, peek second.
The lessons for this chapter are in basics/13_standard_library/.
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

def top_words(text: str, n: int) -> list[tuple[str, int]]:
    """Return the n most common words in text with their counts.

    Split on whitespace, strip the punctuation .,!?;: from both ends of each
    word, lowercase it, and skip anything left empty. collections.Counter
    and its most_common(n) method do the rest (ties keep first-seen order).

    >>> top_words("The cat. The dog! the END", 2)
    [('the', 3), ('cat', 1)]
    """
    raise NotImplementedError


def test_top_words(impl: Callable[[str, int], list[tuple[str, int]]]) -> None:
    got = impl("The cat. The dog! the END", 2)
    assert got == [("the", 3), ("cat", 1)], f"got {got}"
    text = "a b a c b a d; ...  b? A!"
    got = impl(text, 3)
    assert got == [("a", 4), ("b", 3), ("c", 1)], f"for {text!r} got {got}"
    assert impl("", 5) == [], "empty text has no words"
    assert impl("hi hi", 10) == [("hi", 2)], "n larger than the vocabulary is fine"


def check_top_words() -> None:
    report("1. top_words", test_top_words, top_words)


def main() -> None:
    check_top_words()


if __name__ == "__main__":
    main()

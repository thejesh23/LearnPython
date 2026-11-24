"""Password tools: generate strong passwords and judge how strong one is.

You build three tools. A generator that uses the `secrets` module and takes
options (length, which character classes, avoid look-alike characters), plus
a passphrase generator. A checker that applies simple rules and lists what is
wrong. An entropy estimate that turns "how many guesses would it take?" into a
number of bits. The last stage shows, by actually cracking one, why passwords
must never come from the `random` module.

Entropy in one paragraph: if a password is picked uniformly from N equally
likely possibilities, it has log2(N) bits of entropy, and an attacker needs
about N / 2 guesses on average. Every extra bit doubles the work. 16 random
characters from 94 symbols is about 105 bits; "Summer2024!" looks varied but
is one of the first things a cracking tool tries.

Uses:
    02_types               int and float maths, bool results
    04_strings             string constants, membership, f-strings
    06_functions           keyword-only options with defaults
    07_collections         sets of characters, list building
    09_classes             a dataclass for the check result
    11_errors              ValueError for impossible options
    13_standard_library    secrets, math.log2, re, random (and its weakness)
"""

import re
import secrets
import string
from dataclasses import dataclass
from dataclasses import field


# Characters that are easy to confuse when a password is read aloud or typed
# from a printout: O/0, l/1/I and friends.
AMBIGUOUS = set("O0oIl1|`'\"")

WORDLIST = """
acorn amber anchor apple arrow aspen badge bamboo basil beacon berry bison
blossom bridge brook cactus canyon carpet cedar cherry cinder clover cobalt
comet copper coral cotton crater cricket daisy delta desert dolphin dragon
ember falcon fern fiddle forest fossil garnet geyser ginger glacier granite
harbor hazel helmet heron honey island ivory jacket jasper jungle kettle
lagoon lantern lemon lilac lotus magnet maple marble meadow meteor mint
""".split()


def generate_password(
    length: int = 16,
    *,
    upper: bool = True,
    digits: bool = True,
    symbols: bool = True,
    avoid_ambiguous: bool = False,
) -> str:
    """Build a random password that contains every requested character class."""
    classes = [string.ascii_lowercase]
    if upper:
        classes.append(string.ascii_uppercase)
    if digits:
        classes.append(string.digits)
    if symbols:
        classes.append(string.punctuation)
    if avoid_ambiguous:
        classes = ["".join(c for c in cls if c not in AMBIGUOUS) for cls in classes]
    if length < len(classes):
        raise ValueError(f"length {length} is too short for {len(classes)} classes")

    # One guaranteed character from each class, the rest from all of them.
    chars = [secrets.choice(cls) for cls in classes]
    pool = "".join(classes)
    chars += [secrets.choice(pool) for _ in range(length - len(chars))]
    # Shuffle so the guaranteed characters are not always at the front.
    # SystemRandom draws from the same OS source as secrets.
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def generate_passphrase(words: int = 5, separator: str = "-") -> str:
    """Several random words: long, strong and easy to type."""
    return separator.join(secrets.choice(WORDLIST) for _ in range(words))


def describe(password: str) -> str:
    """Which character classes a password contains."""
    found = [
        name
        for name, cls in [
            ("lower", string.ascii_lowercase),
            ("upper", string.ascii_uppercase),
            ("digit", string.digits),
            ("symbol", string.punctuation),
        ]
        if any(c in cls for c in password)
    ]
    return "+".join(found)


def generator_demo() -> None:
    print("== stage 1: generating ==")
    # The passwords differ on every run; that is the point. The properties
    # printed next to them do not.
    for options in [
        {},
        {"length": 12, "symbols": False},
        {"length": 20, "avoid_ambiguous": True},
    ]:
        pw = generate_password(**options)
        print(f"{str(options):<40} {pw}")
        print(f"{'':<40} length {len(pw)}, has {describe(pw)}")
    print(f"passphrase: {generate_passphrase()}")

    many = {generate_password() for _ in range(1000)}
    print(f"1000 passwords, all different: {len(many) == 1000}")
    clean = generate_password(200, avoid_ambiguous=True)
    print(f"no ambiguous characters in 200: {not AMBIGUOUS & set(clean)}")
    try:
        generate_password(3)
    except ValueError as exc:
        print(f"ValueError: {exc}")


# A real checker would use a list of millions of leaked passwords. These are
# a few of the most common ones, all lower case.
COMMON = {"password", "123456", "qwerty", "letmein", "iloveyou", "admin", "welcome"}

KEYBOARD_RUNS = ["abcdefghijklmnopqrstuvwxyz", "0123456789", "qwertyuiop", "asdfghjkl"]


@dataclass
class CheckResult:
    password: str
    problems: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems


def has_sequence(password: str, size: int = 4) -> bool:
    """True if the password contains a run like 'abcd', '1234' or 'qwer'."""
    lowered = password.lower()
    for run in KEYBOARD_RUNS:
        for start in range(len(run) - size + 1):
            if run[start : start + size] in lowered:
                return True
    return False


def check(password: str, min_length: int = 12) -> CheckResult:
    result = CheckResult(password)
    if len(password) < min_length:
        result.problems.append(f"shorter than {min_length} characters")
    # Strip digits and symbols so "Password123!" is still caught.
    core = re.sub(r"[^a-z]", "", password.lower())
    if password.lower() in COMMON or core in COMMON:
        result.problems.append("a well-known common password")
    if has_sequence(password):
        result.problems.append("contains a keyboard or alphabet sequence")
    # (.)\1\1 means: any character, then the same character twice more.
    if re.search(r"(.)\1\1", password):
        result.problems.append("repeats one character three times in a row")
    if re.search(r"(19|20)\d\d", password):
        result.problems.append("contains what looks like a year")
    if len(set(password)) < 6:
        result.problems.append("uses fewer than 6 different characters")
    return result


def checker_demo() -> None:
    print("== stage 2: checking rules ==")
    samples = [
        "Password123!",
        "aaaabbbb",
        "Summer2024!",
        "qwerty7Zx!pq",
        "correct-horse-battery-staple",
        generate_password(),
    ]
    for pw in samples:
        result = check(pw)
        # Do not echo the random one; show only that it passed.
        shown = pw if pw in samples[:-1] else "(generated)"
        print(f"{shown:<30} {'ok' if result.ok else 'problems:'}")
        for problem in result.problems:
            print(f"    - {problem}")


def main() -> None:
    generator_demo()
    print()
    checker_demo()


if __name__ == "__main__":
    main()

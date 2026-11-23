"""Integer arithmetic done by hand: gcd/lcm, fast powers, roots, counting, bases.

Every function works on Python's unbounded ints, so results stay exact where
float-based shortcuts (``n ** 0.5``, ``math.factorial(n) / ...``) would drift.
"""

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def gcd(*values: int) -> int:
    """Greatest common divisor of any number of ints, by Euclid's algorithm."""
    result = 0  # gcd(0, x) == x, so 0 is the identity
    for b in values:
        a, b = result, abs(b)
        while b:
            a, b = b, a % b
        result = a
    return result


def lcm(*values: int) -> int:
    """Least common multiple; 0 if any value is 0, 1 for no values."""
    result = 1
    for v in values:
        if v == 0:
            return 0
        result = result // gcd(result, v) * abs(v)  # divide first to stay small
    return result


def power_mod(base: int, exp: int, mod: int) -> int:
    """base ** exp % mod by square-and-multiply: O(log exp) multiplications."""
    if mod <= 0 or exp < 0:
        raise ValueError("need mod > 0 and exp >= 0")
    result, base = 1 % mod, base % mod
    while exp:
        if exp & 1:  # this bit of the exponent is set: fold in the factor
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


def isqrt(n: int) -> int:
    """floor(sqrt(n)) by Newton's method on integers, exact for any size."""
    if n < 0:
        raise ValueError("isqrt is undefined for negative n")
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + 1) // 2)  # a power of two that is >= sqrt(n)
    while True:
        y = (x + n // x) // 2
        if y >= x:  # the sequence stops decreasing exactly at the answer
            return x
        x = y


def comb(n: int, r: int) -> int:
    """n choose r, keeping every intermediate no bigger than the answer."""
    if not 0 <= r <= n:
        return 0
    r = min(r, n - r)
    result = 1
    for k in range(1, r + 1):
        result = result * (n - k + 1) // k  # result is C(n, k-1): always divisible
    return result


def to_base(n: int, base: int) -> str:
    """Render n in base 2..36 by repeated division."""
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    digits, m = [], abs(n)
    while True:
        m, d = divmod(m, base)
        digits.append(DIGITS[d])
        if not m:
            break
    return ("-" if n < 0 else "") + "".join(reversed(digits))


def from_base(text: str, base: int) -> int:
    """Parse a base 2..36 string back to an int with Horner's method."""
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    text = text.strip().lower()
    sign = -1 if text.startswith("-") else 1
    if text[:1] in ("+", "-"):
        text = text[1:]
    if not text:
        raise ValueError("no digits to parse")
    value = 0
    for ch in text:
        digit = DIGITS.find(ch)
        if not 0 <= digit < base:
            raise ValueError(f"{ch!r} is not a digit in base {base}")
        value = value * base + digit
    return sign * value

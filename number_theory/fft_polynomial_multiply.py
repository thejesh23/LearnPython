"""FFT: multiply two polynomials (or big integers) in O(n log n).

Multiplying polynomials directly is O(n^2) — every coefficient against every
other. The fast Fourier transform sidesteps that by evaluating both polynomials
at the 2n complex roots of unity, where multiplication is pointwise and O(n),
then interpolating back with an inverse transform. Convolution in coefficient
space is a product in value space; the FFT is just a fast change of basis
between them.

The recursive Cooley-Tukey step splits a polynomial into even and odd powers,
each of half the size, and combines them with the "butterfly" using the
symmetry w^(k + n/2) = -w^k. Numbers are floats, so results are rounded back to
integers; for exact integer work use a number-theoretic transform instead.

O(n log n) time.
"""

import cmath


def fft(coeffs: list[complex], invert: bool) -> list[complex]:
    n = len(coeffs)
    if n == 1:
        return coeffs
    even = fft(coeffs[0::2], invert)
    odd = fft(coeffs[1::2], invert)
    angle = (2 if invert else -2) * cmath.pi / n
    out = [0j] * n
    w, step = 1 + 0j, cmath.rect(1, angle)
    for k in range(n // 2):
        out[k] = even[k] + w * odd[k]
        out[k + n // 2] = even[k] - w * odd[k]  # symmetry: w^(k+n/2) = -w^k
        w *= step
    return out


def multiply(a: list[int], b: list[int]) -> list[int]:
    """Polynomial product; coefficient i is sum(a[j]*b[i-j])."""
    size = 1
    while size < len(a) + len(b):
        size *= 2  # FFT wants a power-of-two length
    fa = fft([complex(x) for x in a] + [0j] * (size - len(a)), invert=False)
    fb = fft([complex(x) for x in b] + [0j] * (size - len(b)), invert=False)
    fc = [x * y for x, y in zip(fa, fb)]  # pointwise product in value space
    inverse = fft(fc, invert=True)
    result = [round(z.real / size) for z in inverse]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def multiply_big_integers(x: int, y: int, base: int = 10) -> int:
    """Big-integer multiply by treating the digits as polynomial coefficients."""
    def digits(n: int) -> list[int]:
        out = []
        while n:
            out.append(n % base)
            n //= base
        return out or [0]

    product = multiply(digits(x), digits(y))
    carry, value, place = 0, 0, 1
    for coeff in product:  # resolve carries: coefficients can exceed the base
        total = coeff + carry
        value += (total % base) * place
        carry = total // base
        place *= base
    while carry:
        value += (carry % base) * place
        carry //= base
        place *= base
    return value


def naive_multiply(a: list[int], b: list[int]) -> list[int]:
    result = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def main() -> None:
    # (1 + 2x + 3x^2) * (4 + 5x) = 4 + 13x + 22x^2 + 15x^3
    a, b = [1, 2, 3], [4, 5]
    print(f"FFT product:   {multiply(a, b)}")
    print(f"naive product: {naive_multiply(a, b)}")

    # Cross-check against the naive method on random-ish inputs.
    import random

    rng = random.Random(0)
    ok = True
    for _ in range(50):
        p = [rng.randint(0, 9) for _ in range(rng.randint(1, 20))]
        q = [rng.randint(0, 9) for _ in range(rng.randint(1, 20))]
        expected = naive_multiply(p, q)
        while len(expected) > 1 and expected[-1] == 0:
            expected.pop()
        if multiply(p, q) != expected:
            ok = False
    print(f"matches naive on 50 random polynomials: {ok}")

    x, y = 123456789, 987654321
    print(f"big integer multiply: {multiply_big_integers(x, y)}")
    print(f"agrees with Python:   {x * y}  ({multiply_big_integers(x, y) == x * y})")


if __name__ == "__main__":
    main()

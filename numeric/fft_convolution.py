"""Fast convolution of signals via the FFT.

Convolving two length-n signals directly costs O(n^2): every output sample is a
sum over all shifted products. The convolution theorem turns that into
pointwise multiplication in the frequency domain, so transforming both signals,
multiplying spectrum by spectrum, and transforming back costs only O(n log n).
The transform used here is the radix-2 Cooley-Tukey FFT, which recursively
splits a signal into its even- and odd-indexed samples.

To convolve without the circular wrap-around that a plain DFT product would
cause, both signals are zero-padded to at least len(a)+len(b)-1 and then up to
the next power of two. The result is the ordinary linear convolution, the same
operation a moving-average or any FIR filter performs. Everything is cross-
checked against the naive double loop, and a boxcar kernel is used to smooth a
noisy signal so the filtering interpretation is concrete.
"""

import cmath
import math

Complex = complex


def fft(a: list[Complex], invert: bool = False) -> list[Complex]:
    """Radix-2 Cooley-Tukey FFT; len(a) must be a power of two."""
    n = len(a)
    if n == 1:
        return a[:]
    even = fft(a[0::2], invert)
    odd = fft(a[1::2], invert)
    sign = 1 if invert else -1
    result = [0j] * n
    for k in range(n // 2):
        w = cmath.exp(sign * 2j * math.pi * k / n) * odd[k]
        result[k] = even[k] + w
        result[k + n // 2] = even[k] - w
    # The inverse 1/n normalisation is applied once by the caller, not here.
    return result


def _next_pow2(n: int) -> int:
    p = 1
    while p < n:
        p *= 2
    return p


def convolve_fft(a: list[float], b: list[float]) -> list[float]:
    """Linear convolution of a and b in O(n log n)."""
    out_len = len(a) + len(b) - 1
    size = _next_pow2(out_len)
    fa = fft([complex(x) for x in a] + [0j] * (size - len(a)))
    fb = fft([complex(x) for x in b] + [0j] * (size - len(b)))
    fc = [fa[i] * fb[i] for i in range(size)]
    conv = fft(fc, invert=True)
    return [conv[i].real / size for i in range(out_len)]


def convolve_naive(a: list[float], b: list[float]) -> list[float]:
    """Reference O(n^2) linear convolution."""
    out = [0.0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def main() -> None:
    a = [1.0, 2.0, 3.0, 4.0]
    b = [1.0, 1.0, 1.0]  # summing (unnormalised moving) window of width 3

    fast = convolve_fft(a, b)
    slow = convolve_naive(a, b)
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"fft convolution:   {[round(x, 4) for x in fast]}")
    print(f"naive convolution: {[round(x, 4) for x in slow]}")
    err = max(abs(f - s) for f, s in zip(fast, slow))
    print(f"max |fft - naive|: {err:.2e}")

    # Larger random check against the naive baseline.
    import random

    rng = random.Random(7)
    x = [rng.uniform(-1, 1) for _ in range(50)]
    h = [rng.uniform(-1, 1) for _ in range(30)]
    big_err = max(abs(f - s) for f, s in
                  zip(convolve_fft(x, h), convolve_naive(x, h)))
    print(f"\n50 * 30 random convolution, max error: {big_err:.2e}")

    # Moving-average filter: smooth a noisy sine with a normalised boxcar.
    n = 40
    clean = [math.sin(2 * math.pi * i / n) for i in range(n)]
    noisy = [clean[i] + rng.uniform(-0.4, 0.4) for i in range(n)]
    width = 5
    kernel = [1.0 / width] * width
    smoothed_full = convolve_fft(noisy, kernel)
    # Keep the 'valid' centre so lengths line up with the clean signal.
    start = width // 2
    smoothed = smoothed_full[start:start + n]
    rough = sum((noisy[i] - clean[i]) ** 2 for i in range(n)) / n
    fine = sum((smoothed[i] - clean[i]) ** 2 for i in range(n)) / n
    print(f"\nmoving-average smoothing (width {width})")
    print(f"  mean-squared error, noisy vs clean:    {rough:.5f}")
    print(f"  mean-squared error, smoothed vs clean: {fine:.5f}")
    print(f"  smoothing reduced the error: {fine < rough}")


if __name__ == "__main__":
    main()

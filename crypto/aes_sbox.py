"""The AES S-box: the one nonlinear step, built from GF(2^8) arithmetic.

AES treats each byte as an element of the finite field GF(2^8). Its substitution
box — the S-box — is what makes the cipher nonlinear and resistant to linear and
differential cryptanalysis. Each byte is transformed in two stages: take its
multiplicative inverse in the field (0 maps to 0), then apply a fixed affine
transformation over GF(2), which is a bit rotation-and-XOR pattern.

Field multiplication is "carry-less": multiply as polynomials, then reduce
modulo the AES polynomial x^8 + x^4 + x^3 + x + 1 (0x11B) whenever the result
overflows 8 bits. The inverse is found by exponentiating to the 254th power,
since a^254 = a^(-1) in a field of 256 elements.

This computes the standard S-box from first principles and checks it against the
published table. Educational; real AES uses precomputed tables or hardware.
"""

AES_POLY = 0x11B  # x^8 + x^4 + x^3 + x + 1


def gf_mul(a: int, b: int) -> int:
    """Multiply two bytes in GF(2^8) mod the AES polynomial."""
    result = 0
    while b:
        if b & 1:
            result ^= a  # addition in GF(2^8) is XOR
        b >>= 1
        a <<= 1
        if a & 0x100:  # overflowed 8 bits: reduce
            a ^= AES_POLY
    return result


def gf_inverse(a: int) -> int:
    """Multiplicative inverse via a^254 (Fermat in GF(256)); 0 maps to 0."""
    if a == 0:
        return 0
    result = 1
    for _ in range(254):
        result = gf_mul(result, a)
    return result


def rotl8(x: int, shift: int) -> int:
    return ((x << shift) | (x >> (8 - shift))) & 0xFF


def sbox_byte(a: int) -> int:
    inv = gf_inverse(a)
    # Affine transform: XOR of rotations, plus the constant 0x63.
    return inv ^ rotl8(inv, 1) ^ rotl8(inv, 2) ^ rotl8(inv, 3) ^ rotl8(inv, 4) ^ 0x63


def build_sbox() -> list[int]:
    return [sbox_byte(a) for a in range(256)]


def build_inverse_sbox(sbox: list[int]) -> list[int]:
    inverse = [0] * 256
    for a, s in enumerate(sbox):
        inverse[s] = a
    return inverse


def main() -> None:
    # A few known S-box entries from the AES standard.
    known = {0x00: 0x63, 0x01: 0x7C, 0x53: 0xED, 0x10: 0xCA, 0xFF: 0x16}
    for inp, expected in known.items():
        got = sbox_byte(inp)
        print(f"  S-box[{inp:#04x}] = {got:#04x} (expected {expected:#04x}) "
              f"{'ok' if got == expected else 'WRONG'}")

    sbox = build_sbox()

    # It is a permutation: every output value appears exactly once.
    print(f"S-box is a bijection: {sorted(sbox) == list(range(256))}")

    # The inverse S-box undoes it.
    inv_sbox = build_inverse_sbox(sbox)
    print(f"inverse undoes S-box: {all(inv_sbox[sbox[a]] == a for a in range(256))}")

    # Field arithmetic sanity: a * a^(-1) = 1 for every non-zero byte.
    ok = all(gf_mul(a, gf_inverse(a)) == 1 for a in range(1, 256))
    print(f"every non-zero byte times its inverse is 1: {ok}")

    # No fixed points near the identity — part of why the affine constant exists.
    fixed = [a for a in range(256) if sbox[a] == a]
    print(f"fixed points (S-box[a] == a): {fixed} (none, by design)")

    print(f"first 8 S-box bytes: {[hex(x) for x in sbox[:8]]}")


if __name__ == "__main__":
    main()

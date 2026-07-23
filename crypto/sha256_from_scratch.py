"""SHA-256 from scratch — the Merkle-Damgard construction, step by step.

A cryptographic hash squeezes any input into a fixed 256-bit digest with three
properties: the same input always gives the same output, a different input
almost certainly gives a different output, and you cannot run it backwards or
find two inputs that collide.

SHA-256 works in 512-bit blocks. The message is padded (a 1 bit, then zeros,
then the 64-bit length) so its length is a multiple of 512. Eight 32-bit state
words start from fixed constants; each block runs 64 rounds mixing the block's
words into that state with rotations, shifts, XORs and additions. The final
state is the digest. This is the Merkle-Damgard chaining that HMAC exists to
wrap safely.

This matches hashlib.sha256 byte for byte. Educational only — use hashlib.
"""

# First 32 bits of the fractional parts of the cube roots of the first 64 primes.
K = [
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1,
    0x923F82A4, 0xAB1C5ED5, 0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
    0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174, 0xE49B69C1, 0xEFBE4786,
    0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147,
    0x06CA6351, 0x14292967, 0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
    0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85, 0xA2BFE8A1, 0xA81A664B,
    0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A,
    0x5B9CCA4F, 0x682E6FF3, 0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
    0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
]

MASK = 0xFFFFFFFF


def rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK


def sha256(message: bytes) -> bytes:
    h = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
         0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]

    # Padding: append 0x80, then zeros, then the 64-bit bit-length.
    length_bits = len(message) * 8
    padded = message + b"\x80"
    padded += b"\x00" * ((56 - len(padded) % 64) % 64)
    padded += length_bits.to_bytes(8, "big")

    for block_start in range(0, len(padded), 64):
        block = padded[block_start:block_start + 64]
        w = list(int.from_bytes(block[i:i + 4], "big") for i in range(0, 64, 4))
        # Extend the 16 block words into 64.
        for i in range(16, 64):
            s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w.append((w[i - 16] + s0 + w[i - 7] + s1) & MASK)

        a, b, c, d, e, f, g, hh = h
        for i in range(64):
            s1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (hh + s1 + ch + K[i] + w[i]) & MASK
            s0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (s0 + maj) & MASK
            a, b, c, d, e, f, g, hh = (
                (temp1 + temp2) & MASK, a, b, c, (d + temp1) & MASK, e, f, g)

        for i, value in enumerate((a, b, c, d, e, f, g, hh)):
            h[i] = (h[i] + value) & MASK

    return b"".join(x.to_bytes(4, "big") for x in h)


def main() -> None:
    import hashlib

    cases = [b"", b"abc", b"hello world", b"The quick brown fox jumps over the lazy dog"]
    for message in cases:
        mine = sha256(message).hex()
        reference = hashlib.sha256(message).hexdigest()
        label = message[:20].decode() or "(empty)"
        print(f"  {label:<22} match={mine == reference} {mine[:24]}...")

    # Exactly one block, exactly on the padding boundary, and multi-block.
    for size in (0, 55, 56, 64, 100, 1000):
        data = b"x" * size
        ok = sha256(data) == hashlib.sha256(data).digest()
        print(f"  {size:>4}-byte input matches stdlib: {ok}")

    # The avalanche property: one flipped input bit changes about half the output.
    a = sha256(b"message")
    b = sha256(b"messagf")  # last byte off by one bit
    diff = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
    print(f"one input bit flipped -> {diff}/256 output bits changed (~half)")

    print(f"empty string digest: {sha256(b'').hex()}")


if __name__ == "__main__":
    main()

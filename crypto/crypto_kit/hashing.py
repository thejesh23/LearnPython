"""SHA-256 from scratch, HMAC built on it, and a Merkle tree with membership proofs.

Toy / educational code: it matches hashlib and hmac byte for byte, but it is
slow and not hardened. Real code uses hashlib, hmac and hmac.compare_digest.
"""

# First 32 bits of the fractional parts of the cube roots of the first 64 primes.
_K = [
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
]
_MASK = 0xFFFFFFFF
BLOCK_SIZE = 64  # bytes per SHA-256 block


def _rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & _MASK


def sha256(message: bytes) -> bytes:
    """The 32-byte SHA-256 digest: pad, then mix each 64-byte block into 8 state words."""
    h = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]
    padded = message + b"\x80"
    padded += b"\x00" * (-(len(padded) + 8) % BLOCK_SIZE) + (len(message) * 8).to_bytes(8, "big")
    for start in range(0, len(padded), BLOCK_SIZE):
        w = [int.from_bytes(padded[start + i:start + i + 4], "big") for i in range(0, 64, 4)]
        for i in range(16, 64):
            s0 = _rotr(w[i - 15], 7) ^ _rotr(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = _rotr(w[i - 2], 17) ^ _rotr(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w.append((w[i - 16] + s0 + w[i - 7] + s1) & _MASK)
        a, b, c, d, e, f, g, hh = h
        for i in range(64):
            t1 = hh + (_rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)) + ((e & f) ^ (~e & g)) + _K[i] + w[i]
            t2 = (_rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))
            a, b, c, d, e, f, g, hh = (t1 + t2) & _MASK, a, b, c, (d + t1) & _MASK, e, f, g
        h = [(x + y) & _MASK for x, y in zip(h, (a, b, c, d, e, f, g, hh))]
    return b"".join(x.to_bytes(4, "big") for x in h)


def hmac_sha256(key: bytes, message: bytes) -> bytes:
    """HMAC(k, m) = H((k ^ opad) || H((k ^ ipad) || m)), immune to length extension."""
    if len(key) > BLOCK_SIZE:
        key = sha256(key)
    key = key.ljust(BLOCK_SIZE, b"\x00")
    inner = sha256(bytes(b ^ 0x36 for b in key) + message)
    return sha256(bytes(b ^ 0x5C for b in key) + inner)


def _leaf(data: bytes) -> bytes:
    return sha256(b"\x00" + data)  # 0x00 / 0x01 prefixes stop a node posing as a leaf


def _node(left: bytes, right: bytes) -> bytes:
    return sha256(b"\x01" + left + right)


Proof = list[tuple[bytes, str]]


class MerkleTree:
    """Hash leaves pairwise up to one root; prove membership with O(log n) hashes."""

    def __init__(self, items: list[bytes]) -> None:
        if not items:
            raise ValueError("need at least one item")
        self.levels = [[_leaf(item) for item in items]]
        while len(self.levels[-1]) > 1:
            level = self.levels[-1]
            pairs = [(level[i], level[min(i + 1, len(level) - 1)]) for i in range(0, len(level), 2)]
            self.levels.append([_node(left, right) for left, right in pairs])

    @property
    def root(self) -> bytes:
        """The single hash that commits to every item."""
        return self.levels[-1][0]

    def proof(self, index: int) -> Proof:
        """Sibling hashes from leaf ``index`` up to the root, each tagged left/right."""
        path: Proof = []
        for level in self.levels[:-1]:
            sibling = min(index ^ 1, len(level) - 1)  # a lone last node pairs with itself
            path.append((level[sibling], "left" if index % 2 else "right"))
            index //= 2
        return path


def verify_proof(item: bytes, proof: Proof, root: bytes) -> bool:
    """Rehash from ``item`` along ``proof``; True if we land on ``root``."""
    node = _leaf(item)
    for sibling, side in proof:
        node = _node(sibling, node) if side == "left" else _node(node, sibling)
    return node == root

"""Merkle tree: prove one item belongs to a set with a log-sized proof.

Hash every leaf, then repeatedly hash pairs of hashes up to a single root.
Anyone holding just the root can verify that a given item was in the tree by
being shown only the sibling hash at each level — O(log n) hashes — instead of
the whole dataset. Change any leaf and every hash on the path to the root
changes, so the root commits to the entire contents.

This is the backbone of Git (commit trees), Bitcoin (transaction roots),
Certificate Transparency, and content-addressed storage. The audit proof is
what lets a light client trust a huge dataset it never downloads.

Building the tree is O(n); a membership proof is O(log n) to produce and verify.
A second-preimage guard (domain-separating leaf and internal hashes) prevents an
attacker from passing an internal node off as a leaf.
"""

import hashlib


def _hash_leaf(data: bytes) -> bytes:
    return hashlib.sha256(b"\x00" + data).digest()  # 0x00 tags a leaf


def _hash_node(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(b"\x01" + left + right).digest()  # 0x01 tags a node


class MerkleTree:
    def __init__(self, items: list[bytes]) -> None:
        if not items:
            raise ValueError("need at least one item")
        self.leaves = [_hash_leaf(item) for item in items]
        self.levels = [self.leaves]
        level = self.leaves
        while len(level) > 1:
            nxt = []
            for i in range(0, len(level), 2):
                left = level[i]
                right = level[i + 1] if i + 1 < len(level) else level[i]  # duplicate a lone node
                nxt.append(_hash_node(left, right))
            self.levels.append(nxt)
            level = nxt

    @property
    def root(self) -> bytes:
        return self.levels[-1][0]

    def proof(self, index: int) -> list[tuple[bytes, str]]:
        """Sibling hashes from leaf to root, each tagged left/right."""
        path: list[tuple[bytes, str]] = []
        for level in self.levels[:-1]:
            sibling = index ^ 1  # the other node in the pair
            if sibling < len(level):
                side = "right" if index % 2 == 0 else "left"
                path.append((level[sibling], side))
            else:
                path.append((level[index], "right"))  # the duplicated lone node
            index //= 2
        return path


def verify(item: bytes, proof: list[tuple[bytes, str]], root: bytes) -> bool:
    node = _hash_leaf(item)
    for sibling, side in proof:
        node = _hash_node(sibling, node) if side == "left" else _hash_node(node, sibling)
    return node == root


def main() -> None:
    blocks = [f"transaction {i}".encode() for i in range(8)]
    tree = MerkleTree(blocks)
    print(f"{len(blocks)} leaves, root: {tree.root.hex()[:32]}...")
    print(f"tree height: {len(tree.levels) - 1} levels")

    # Prove membership of one block with a log-sized proof.
    index = 3
    proof = tree.proof(index)
    print(f"proof for leaf {index}: {len(proof)} sibling hashes (log2(8) = 3)")
    print(f"verifies against the root: {verify(blocks[index], proof, tree.root)}")

    # A forged item with the real proof fails.
    print(f"forged item rejected: {not verify(b'transaction 999', proof, tree.root)}")

    # Every leaf verifies with its own proof.
    all_ok = all(verify(blocks[i], tree.proof(i), tree.root) for i in range(len(blocks)))
    print(f"all {len(blocks)} leaves verify: {all_ok}")

    # Changing any leaf changes the root — the tree commits to everything.
    tampered = blocks[:]
    tampered[5] = b"tampered"
    print(f"one leaf changed -> new root differs: {MerkleTree(tampered).root != tree.root}")

    # Odd leaf counts duplicate the last node.
    odd = MerkleTree([b"a", b"b", b"c"])
    print(f"odd count (3 leaves) builds and verifies: "
          f"{verify(b'c', odd.proof(2), odd.root)}")


if __name__ == "__main__":
    main()

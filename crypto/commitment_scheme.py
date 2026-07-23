"""Commitment schemes: seal a value now, reveal it later, cheat neither way.

A commitment is a cryptographic envelope. You publish a commitment to a value,
and later open it. Two properties must hold at once: it is *hiding* (the
commitment reveals nothing about the value) and *binding* (you cannot open it to
any value other than the one you sealed). Think of a sealed bid, a coin flip
over the phone, or the "reveal" phase of a fair lottery.

The simple hash commitment C = H(value || nonce) is hiding when the nonce is
long and random, and binding because finding a second (value, nonce) with the
same hash means a hash collision. The nonce matters: without it, a commitment to
a low-entropy value (like "heads") is trivially brute-forced.

This uses SHA-256 for illustration. Pedersen commitments (shown in prose) add
information-theoretic hiding and additive homomorphism, at the cost of a group.
"""

import hashlib
import secrets


def commit(value: bytes) -> tuple[bytes, bytes]:
    """Return (commitment, nonce). Keep the nonce secret until reveal."""
    nonce = secrets.token_bytes(32)
    commitment = hashlib.sha256(nonce + value).digest()
    return commitment, nonce


def verify(commitment: bytes, value: bytes, nonce: bytes) -> bool:
    return hashlib.sha256(nonce + value).digest() == commitment


def coin_flip_demo() -> str:
    """Fair remote coin flip: each side commits, then both reveal and XOR."""
    alice_bit = secrets.randbelow(2)
    bob_bit = secrets.randbelow(2)
    # Both commit before either reveals, so neither can adapt to the other.
    a_commit, a_nonce = commit(bytes([alice_bit]))
    b_commit, b_nonce = commit(bytes([bob_bit]))
    # Reveal phase; verify the other's opening matches their commitment.
    assert verify(a_commit, bytes([alice_bit]), a_nonce)
    assert verify(b_commit, bytes([bob_bit]), b_nonce)
    result = alice_bit ^ bob_bit  # neither party alone controls the outcome
    return "heads" if result == 0 else "tails"


def main() -> None:
    secret = b"the answer is 42"
    commitment, nonce = commit(secret)
    print(f"published commitment: {commitment.hex()[:32]}...")
    print("(the value stays hidden until the nonce is revealed)")

    print(f"correct opening verifies: {verify(commitment, secret, nonce)}")

    # Binding: you cannot open the same commitment to a different value.
    print(f"opening to a lie fails: {verify(commitment, b'the answer is 7', nonce)}")
    print(f"wrong nonce fails:      {verify(commitment, secret, secrets.token_bytes(32))}")

    # Hiding: a commitment to a low-entropy value leaks nothing WITH a nonce...
    heads_commit, _ = commit(b"heads")
    heads_commit2, _ = commit(b"heads")
    print(f"same value, different commitments (thanks to the nonce): "
          f"{heads_commit != heads_commit2}")

    # ...but WITHOUT a nonce it is trivially brute-forced.
    naive = hashlib.sha256(b"heads").digest()
    guessed = next(g for g in (b"heads", b"tails") if hashlib.sha256(g).digest() == naive)
    print(f"nonce-free commitment brute-forced back to {guessed!r}")

    print("fair remote coin flip via commit-then-reveal:")
    outcomes = [coin_flip_demo() for _ in range(6)]
    print(f"  results: {outcomes}")
    print("  neither party can bias it: both commit before either reveals")

    print("Pedersen commitments add perfect hiding and let you add commitments:")
    print("  C(a) * C(b) = C(a + b), the basis of confidential transactions")


if __name__ == "__main__":
    main()

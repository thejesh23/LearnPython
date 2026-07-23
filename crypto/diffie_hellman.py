"""Diffie-Hellman key exchange — a shared secret over a public channel.

Two parties agree on a public prime p and generator g. Alice picks a secret a
and sends g^a mod p; Bob picks b and sends g^b mod p. Each raises the other's
value to their own secret: (g^b)^a = (g^a)^b = g^(ab) mod p. An eavesdropper
sees g, p, g^a and g^b but recovering g^(ab) requires the discrete logarithm,
which is infeasible for a large safe prime.

The famous weakness is that plain DH authenticates nobody, so it is defenceless
against a man in the middle who swaps in their own keys with each side. Real
protocols sign the exchange or run it inside an authenticated channel.

This is illustrative only; use a vetted library and a standardised group.
"""

import secrets


# A small safe prime for a readable demo (p = 2q + 1, q also prime).
P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A63A3620FFFFFFFFFFFFFFFF
G = 2


def public_value(secret: int, p: int = P, g: int = G) -> int:
    return pow(g, secret, p)


def shared_secret(their_public: int, my_secret: int, p: int = P) -> int:
    return pow(their_public, my_secret, p)


def derive_key(shared: int) -> str:
    """A real protocol runs the shared integer through a KDF, not raw."""
    import hashlib

    return hashlib.sha256(shared.to_bytes((shared.bit_length() + 7) // 8, "big")).hexdigest()


def main() -> None:
    print(f"public parameters: {P.bit_length()}-bit prime, generator g = {G}")

    alice_secret = secrets.randbelow(P - 2) + 1
    bob_secret = secrets.randbelow(P - 2) + 1

    alice_public = public_value(alice_secret)
    bob_public = public_value(bob_secret)
    print("Alice and Bob exchange public values over the open channel")

    alice_shared = shared_secret(bob_public, alice_secret)
    bob_shared = shared_secret(alice_public, bob_secret)
    print(f"both derive the same secret: {alice_shared == bob_shared}")
    print(f"session key: {derive_key(alice_shared)[:32]}...")

    # An eavesdropper with only the public values cannot cheaply reconstruct it.
    print("an eavesdropper sees g, p, g^a, g^b but not g^(ab):")
    print("  recovering it means solving the discrete log — infeasible here")

    # Small parameters make the discrete log tractable, which is why real
    # groups are thousands of bits.
    small_p, small_g = 23, 5
    a, b = 6, 15
    ga, gb = pow(small_g, a, small_p), pow(small_g, b, small_p)
    print(f"toy group p=23: g^a={ga}, g^b={gb}, "
          f"shared={pow(gb, a, small_p)}=={pow(ga, b, small_p)}")

    # Man-in-the-middle: DH alone proves nothing about who is on the other end.
    print("man-in-the-middle: unauthenticated DH lets an attacker sit between")
    mallory_secret = secrets.randbelow(small_p - 2) + 1
    mallory_public = pow(small_g, mallory_secret, small_p)
    alice_thinks = pow(mallory_public, a, small_p)
    mallory_with_alice = pow(ga, mallory_secret, small_p)
    print(f"  Alice shares {alice_thinks} with Mallory, not Bob: "
          f"{alice_thinks == mallory_with_alice}")
    print("  fix: sign the public values (authenticated DH)")


if __name__ == "__main__":
    main()

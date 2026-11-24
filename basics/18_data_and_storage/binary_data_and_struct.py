"""Binary data: `bytes`, `bytearray`, byte order and the `struct` module.

Text files store characters. Many real formats (images, audio, network
packets, the header of a zip file) store raw numbers instead: the number
1000 as the two bytes 0x03 0xE8 rather than the four characters "1000".
Python handles this with

    bytes          an immutable sequence of numbers 0-255
    bytearray      the same, but changeable in place
    int.to_bytes   one integer to bytes, and int.from_bytes back
    struct         many values at once, described by a format string

Byte order ("endianness") is the catch: a number that needs several bytes can
be stored biggest byte first (big-endian, used by network protocols) or
smallest byte first (little-endian, used by most CPUs). Both sides must agree,
so a file format always says which one it uses, and so should your code.
"""

import struct
import sys


def bytes_demo() -> None:
    # Text becomes bytes through an encoding; bytes become text by decoding.
    data = "héllo".encode("utf-8")
    print(f"'héllo' in UTF-8: {data!r}, {len(data)} bytes for 5 characters")
    print(f"decoded again: {data.decode('utf-8')!r}")

    # Indexing bytes gives an int; slicing gives bytes.
    print(f"data[0] = {data[0]} (the code for 'h'), data[:1] = {data[:1]!r}")
    print(f"as hex: {data.hex(' ')}")
    print(f"from hex: {bytes.fromhex('48 69 21')!r}")
    print(f"from a list of ints: {bytes([80, 121, 116, 104, 111, 110])!r}")

    # bytes cannot change; bytearray can.
    try:
        data[0] = 72  # type: ignore[index]
    except TypeError:
        print("bytes are immutable: item assignment -> TypeError")
    buffer = bytearray(b"hello")
    buffer[0] = ord("j")
    buffer.extend(b" world")
    print(f"bytearray after edits: {buffer!r} -> {bytes(buffer)!r}")
    try:
        buffer.append(256)
    except ValueError as exc:
        print(f"each item must fit in a byte: ValueError: {exc}")


def endianness_demo() -> None:
    n = 1000  # 0x03E8
    big = n.to_bytes(4, "big")
    little = n.to_bytes(4, "little")
    print(f"{n} as 4 bytes, big-endian:    {big.hex(' ')}")
    print(f"{n} as 4 bytes, little-endian: {little.hex(' ')}")

    # Reading with the wrong byte order gives a wrong number, not an error.
    print(f"read back correctly: {int.from_bytes(little, 'little')}")
    print(f"read with the wrong order: {int.from_bytes(little, 'big')}")

    # Negative numbers need signed=True (two's complement).
    print(f"-2 as a signed byte: {(-2).to_bytes(1, 'big', signed=True).hex()}")
    try:
        (300).to_bytes(1, "big")
    except OverflowError:
        print("300 does not fit in 1 byte -> OverflowError")

    # Your CPU has a native order, but a file format should not depend on it.
    print(f"this machine is {sys.byteorder}-endian")


def struct_demo() -> None:
    # The first character sets the byte order: '<' little, '>' or '!' big.
    # Then one letter per value: B = unsigned 1-byte, H = 2-byte,
    # I = 4-byte, i = signed 4-byte, f = 4-byte float, 4s = 4 raw bytes.
    fmt = "<HIf4s"
    packed = struct.pack(fmt, 7, 1000, 2.5, b"abcd")
    print(f"pack({fmt!r}) -> {len(packed)} bytes: {packed.hex(' ')}")
    print(f"calcsize says {struct.calcsize(fmt)} bytes")
    print(f"unpack -> {struct.unpack(fmt, packed)}  (always a tuple)")

    # A 4-byte float cannot hold 0.1 exactly; the value comes back rounded.
    (approx,) = struct.unpack("<f", struct.pack("<f", 0.1))
    print(f"0.1 through a 4-byte float: {approx}")

    # Without '<' or '>' struct uses native order AND inserts padding so
    # each field is aligned, which is why explicit order is the safe habit.
    print(f"native '@BI' is {struct.calcsize('@BI')} bytes, '<BI' is "
          f"{struct.calcsize('<BI')} bytes")

    try:
        struct.pack("<B", 300)
    except struct.error as exc:
        print(f"out of range: struct.error: {exc}")


def main() -> None:
    bytes_demo()
    print()
    endianness_demo()
    print()
    struct_demo()


if __name__ == "__main__":
    main()

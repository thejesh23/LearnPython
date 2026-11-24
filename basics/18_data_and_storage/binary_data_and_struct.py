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


def main() -> None:
    bytes_demo()


if __name__ == "__main__":
    main()

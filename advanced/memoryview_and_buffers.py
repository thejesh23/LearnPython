"""`memoryview` — slicing bytes without copying them.

`data[1000:2000]` on a bytes object allocates a new 1000-byte object. A
memoryview exposes the same buffer through a window: slicing it is O(1) and
allocates nothing. For parsing large binary blobs, that is the difference
between one allocation and thousands.

`bytearray` is the mutable sibling, and a memoryview over one can write through
to the original. `struct` packs and unpacks fixed binary layouts.
"""

import struct
import sys


def main() -> None:
    data = bytes(range(256)) * 100  # 25.6 KB
    print(f"buffer: {len(data)} bytes")

    copy = data[1000:2000]
    view = memoryview(data)[1000:2000]
    print(f"slice copy   -> {sys.getsizeof(copy)} bytes allocated")
    print(f"memoryview   -> {sys.getsizeof(view)} bytes (a window, not a copy)")
    print(f"same content: {bytes(view) == copy}")

    # Writing through a view mutates the underlying bytearray.
    buffer = bytearray(b"hello world")
    window = memoryview(buffer)[0:5]
    window[0:5] = b"HELLO"
    print(f"after writing through the view: {buffer!r}")

    # A view can be reinterpreted without copying.
    numbers = memoryview(bytearray(struct.pack("<4i", 1, 2, 3, 4)))
    as_ints = numbers.cast("i")
    print(f"cast to int32: {list(as_ints)}, itemsize={as_ints.itemsize}")

    # struct: fixed binary layouts. '<' little-endian, 'I' uint32, 'H' uint16.
    header = struct.pack("<IHH", 0xDEADBEEF, 1, 512)
    magic, version, size = struct.unpack("<IHH", header)
    print(f"packed {len(header)} bytes -> magic=0x{magic:X} version={version} size={size}")
    print(f"struct.calcsize('<IHH') = {struct.calcsize('<IHH')}")

    # Zero-copy parsing: walk records through views.
    records = b"".join(struct.pack("<IH", i, i * 2) for i in range(5))
    mv = memoryview(records)
    parsed = [struct.unpack_from("<IH", mv, off) for off in range(0, len(records), 6)]
    print(f"parsed without copying: {parsed}")

    # Views keep the underlying buffer alive and locked against resizing.
    ba = bytearray(b"abc")
    keep = memoryview(ba)
    try:
        ba.extend(b"def")
    except BufferError as exc:
        print(f"BufferError: {exc}")
    keep.release()
    ba.extend(b"def")
    print(f"after release: {ba!r}")


if __name__ == "__main__":
    main()

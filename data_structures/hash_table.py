"""A hash table from scratch: buckets, collisions, and resizing.

Three pieces decide everything:
  hashing     map a key to a bucket index (`hash(key) % capacity`)
  collisions  two keys landing in the same bucket — resolved here by chaining
  load factor  entries / buckets; past ~0.75 collisions dominate, so grow and
               rehash everything into a larger table

Amortised O(1) per operation; O(n) in the worst case when every key collides.
Python's own dict uses open addressing with perturbed probing plus a compact
insertion-ordered entry array — different mechanics, same contract.
"""


class HashTable:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.buckets: list[list[tuple[object, object]]] = [[] for _ in range(capacity)]

    def _index(self, key: object) -> int:
        return hash(key) % self.capacity

    def put(self, key: object, value: object) -> None:
        bucket = self.buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # overwrite
                return
        bucket.append((key, value))
        self.size += 1
        if self.size / self.capacity > 0.75:
            self._resize()

    def get(self, key: object, default: object = None) -> object:
        for k, v in self.buckets[self._index(key)]:
            if k == key:
                return v
        return default

    def delete(self, key: object) -> bool:
        bucket = self.buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def _resize(self) -> None:
        old = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old:
            for k, v in bucket:
                self.put(k, v)  # rehash: the index depends on capacity

    def stats(self) -> str:
        used = sum(1 for b in self.buckets if b)
        longest = max((len(b) for b in self.buckets), default=0)
        return (f"{self.size} entries in {self.capacity} buckets, "
                f"{used} used, longest chain {longest}, "
                f"load {self.size / self.capacity:.2f}")

    def __len__(self) -> int:
        return self.size


class BadKey:
    """Every instance hashes the same — the pathological case."""

    def __hash__(self) -> int:
        return 1

    def __eq__(self, other: object) -> bool:
        return self is other


def main() -> None:
    table = HashTable()
    for i in range(12):
        table.put(f"key{i}", i * 10)
    print(f"after 12 inserts: {table.stats()}")
    print(f"get('key7') = {table.get('key7')}, missing -> {table.get('nope', 'default')}")
    table.put("key7", 999)
    print(f"overwrite: {table.get('key7')}, size unchanged: {len(table)}")
    print(f"delete('key0') -> {table.delete('key0')}, size {len(table)}")

    # Every key colliding degrades to a linked list.
    bad = HashTable()
    for _ in range(6):
        bad.put(BadKey(), 1)
    print(f"pathological hashing: {bad.stats()}")

    # Mutable objects cannot be keys, because their hash would change.
    try:
        hash([1, 2])
    except TypeError as exc:
        print(f"unhashable: {exc}")
    print(f"hash stability is the contract: equal objects must hash equally")


if __name__ == "__main__":
    main()

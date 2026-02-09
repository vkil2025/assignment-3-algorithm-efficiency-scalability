
import random
from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class Entry:
    key: int
    value: Any


class HashTableChaining:
    """
    Hash table with chaining for collision resolution.

    Buckets are lists of Entry objects. The hash function uses randomized
    MAD compression:
        h(k) = ((a*k + b) mod p) mod m
    where p is a large prime, and (a, b) are randomized per table instance.
    """

    def __init__(self, capacity: int = 16, load_factor_max: float = 0.75) -> None:
        if capacity < 1:
            capacity = 1

        self._m = 1
        while self._m < capacity:
            self._m <<= 1

        self._buckets: List[List[Entry]] = [[] for _ in range(self._m)]
        self._n = 0
        self._lf_max = float(load_factor_max)

        self._p = 2_147_483_647  # large prime near 2^31-1
        self._a = random.randint(1, self._p - 1)
        self._b = random.randint(0, self._p - 1)

    def _hash(self, key: int) -> int:
        return ((self._a * key + self._b) % self._p) % self._m

    def _rehash(self, new_capacity: int) -> None:
        items = []
        for bucket in self._buckets:
            for e in bucket:
                items.append((e.key, e.value))

        self._m = 1
        while self._m < new_capacity:
            self._m <<= 1
        self._buckets = [[] for _ in range(self._m)]
        self._n = 0

        # Re-randomize hash parameters during resize
        self._a = random.randint(1, self._p - 1)
        self._b = random.randint(0, self._p - 1)

        for k, v in items:
            self.insert(k, v)

    def _maybe_resize(self) -> None:
        if self.load_factor() > self._lf_max:
            self._rehash(self._m * 2)

    def insert(self, key: int, value: Any) -> None:
        idx = self._hash(key)
        bucket = self._buckets[idx]

        for e in bucket:
            if e.key == key:
                e.value = value
                return

        bucket.append(Entry(key, value))
        self._n += 1
        self._maybe_resize()

    def search(self, key: int) -> Optional[Any]:
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for e in bucket:
            if e.key == key:
                return e.value
        return None

    def delete(self, key: int) -> bool:
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, e in enumerate(bucket):
            if e.key == key:
                bucket.pop(i)
                self._n -= 1
                return True
        return False

    def size(self) -> int:
        return self._n

    def capacity(self) -> int:
        return self._m

    def load_factor(self) -> float:
        return self._n / self._m

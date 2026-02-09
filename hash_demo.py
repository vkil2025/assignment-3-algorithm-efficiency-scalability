
from hash_table_chaining import HashTableChaining


def main() -> None:
    ht = HashTableChaining(capacity=8)

    ht.insert(101, "Alice")
    ht.insert(202, "Bob")
    ht.insert(303, "Charlie")

    print("Size:", ht.size())
    print("Capacity:", ht.capacity())
    print("Load factor:", round(ht.load_factor(), 3))

    print("Search 202:", ht.search(202))
    print("Search 999:", ht.search(999))

    ht.insert(202, "Bob Updated")
    print("Search 202 after update:", ht.search(202))

    print("Delete 101:", ht.delete(101))
    print("Search 101:", ht.search(101))
    print("Size:", ht.size())


if __name__ == "__main__":
    main()


# Assignment 3: Understanding Algorithm Efficiency and Scalability

## Contents
1) **Randomized Quicksort** (uniform random pivot) + comparison to
   **Deterministic Quicksort** (first-element pivot). Uses **3-way partitioning**
   to handle repeated elements efficiently.

2) **Hash Table with Chaining** (collision resolution via bucket lists) using
   randomized MAD compression hashing:
   `h(k) = ((a*k + b) mod p) mod m`

## Run
### Quicksort benchmarks
```bash
python3 quicksort_benchmark.py
```

(Optional) write a CSV:
```bash
python3 quicksort_benchmark.py --csv results.csv
```

### Hash demo
```bash
python3 hash_demo.py
```

Tested with Python 3.10+.

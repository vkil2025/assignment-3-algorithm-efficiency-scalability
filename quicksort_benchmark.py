
import argparse
import csv
import random
import time
import sys
from dataclasses import dataclass
from typing import Callable, List, Tuple


def partition_3way(arr: List[int], lo: int, hi: int, pivot_index: int) -> Tuple[int, int]:
    """
    3-way partition around pivot value.
    After partition:
      arr[lo:lt]     < pivot
      arr[lt:gt+1]   = pivot
      arr[gt+1:hi+1] > pivot
    Returns (lt, gt).
    """
    pivot = arr[pivot_index]
    arr[lo], arr[pivot_index] = arr[pivot_index], arr[lo]  # move pivot to front

    lt = lo
    i = lo + 1
    gt = hi

    while i <= gt:
        if arr[i] < pivot:
            lt += 1
            arr[lt], arr[i] = arr[i], arr[lt]
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    arr[lo], arr[lt] = arr[lt], arr[lo]  # pivot to final position
    return lt, gt


def randomized_quicksort(arr: List[int]) -> List[int]:
    """Randomized pivot quicksort with 3-way partitioning."""
    a = arr[:]  # do not mutate caller

    def _qs(lo: int, hi: int) -> None:
        if lo >= hi:
            return
        pivot_index = random.randint(lo, hi)
        lt, gt = partition_3way(a, lo, hi, pivot_index)
        _qs(lo, lt - 1)
        _qs(gt + 1, hi)

    _qs(0, len(a) - 1)
    return a


def deterministic_quicksort_first_pivot(arr: List[int]) -> List[int]:
    """Deterministic quicksort using first element as pivot + 3-way partitioning."""
    a = arr[:]

    def _qs(lo: int, hi: int) -> None:
        if lo >= hi:
            return
        pivot_index = lo
        lt, gt = partition_3way(a, lo, hi, pivot_index)
        _qs(lo, lt - 1)
        _qs(gt + 1, hi)

    _qs(0, len(a) - 1)
    return a


@dataclass
class Case:
    name: str
    generator: Callable[[int], List[int]]


def gen_random(n: int) -> List[int]:
    return [random.randint(0, 10**7) for _ in range(n)]


def gen_sorted(n: int) -> List[int]:
    return list(range(n))


def gen_reverse_sorted(n: int) -> List[int]:
    return list(range(n, 0, -1))


def gen_repeated(n: int) -> List[int]:
    return [random.randint(0, 20) for _ in range(n)]


def time_func(func: Callable[[List[int]], List[int]], arr: List[int], repeats: int = 3) -> float:
    """Best-of-N timing with correctness check."""
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        out = func(arr)
        end = time.perf_counter()
        if out != sorted(arr):
            raise ValueError(f"Sorting failed for {func.__name__}")
        best = min(best, end - start)
    return best


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark randomized vs deterministic Quicksort.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    parser.add_argument("--repeats", type=int, default=3, help="Best-of-N runs per cell.")
    parser.add_argument("--csv", type=str, default="", help="Optional CSV output path (e.g., results.csv).")
    args = parser.parse_args()

    random.seed(args.seed)

    cases = [
        Case("Random", gen_random),
        Case("Sorted", gen_sorted),
        Case("ReverseSorted", gen_reverse_sorted),
        Case("Repeated", gen_repeated),
    ]

    sizes = [1_000, 5_000, 10_000, 20_000, 40_000]
    # Prevent recursion errors for deterministic first-pivot on sorted inputs
    sys.setrecursionlimit(max(10000, max(sizes) * 5))

    algos = [
        ("RandomizedQuicksort", randomized_quicksort),
        ("DeterministicFirstPivot", deterministic_quicksort_first_pivot),
    ]

    print("Benchmark: Randomized Quicksort vs Deterministic First-Pivot Quicksort")
    print(f"Times are best-of-{args.repeats} runs (seconds)\n")

    header = f"{'Case':<15}{'n':>8}" + "".join([f"{name:>28}" for name, _ in algos])
    print(header)
    print("-" * len(header))

    rows = []
    for case in cases:
        for n in sizes:
            base = case.generator(n)
            row = {"case": case.name, "n": n}
            line = f"{case.name:<15}{n:>8}"
            for name, algo in algos:
                t = time_func(algo, base, repeats=args.repeats)
                row[name] = t
                line += f"{t:>28.6f}"
            print(line)
            rows.append(row)
        print()

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["case", "n"] + [name for name, _ in algos]
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)
        print(f"Wrote CSV results to: {args.csv}")

    print("Done.")


if __name__ == "__main__":
    main()

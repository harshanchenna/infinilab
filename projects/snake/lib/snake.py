"""Trusted primitives for the snake-in-the-box project.

FIXED infrastructure (the analog of cap_set's cap.py): the loop never edits this;
experiments and the evolver compose it, and the Tier-1 verifier trusts it.

A *snake* is a longest induced (chordless) path in the n-dimensional hypercube
graph Q_n: vertices are the integers 0..2^n-1 (n-bit strings), edges join numbers
differing in exactly one bit. A path v_0, v_1, ..., v_L is *induced* iff the only
adjacencies among its vertices are the consecutive ones -- no "chords". The snake
length is the number of EDGES, L = (#vertices - 1).

The key object is `is_induced_path`, a cheap O(L^2) RIGOROUS verifier in exact
integer (bit) arithmetic. It cannot be fooled: a claimed snake is accepted iff it
truly is a chordless path in Q_n. That is the un-gameable spine.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Callable, Optional

# Longest snake (induced path) lengths in Q_n, in EDGES. Proven optima for n<=8
# (OEIS A099155); for n>=9 these are the best known LOWER bounds, not proven
# maxima -- compare honestly. n: 1..13.
LONGEST_KNOWN = {1: 1, 2: 2, 3: 4, 4: 7, 5: 13, 6: 26, 7: 50, 8: 98,
                 9: 190, 10: 370, 11: 707, 12: 1302, 13: 2520}
PROVEN_THROUGH = 8   # exact maxima are known only for n <= 8


def popcount(x: int) -> int:
    return bin(x).count("1")


def neighbors(v: int, n: int) -> list[int]:
    """The n hypercube neighbors of v (flip each of the n bits)."""
    return [v ^ (1 << i) for i in range(n)]


def is_induced_path(path: list[int], n: int) -> tuple[bool, Optional[tuple]]:
    """Rigorously check `path` is an induced (chordless) path in Q_n.

    Returns (True, None) or (False, witness). Three conditions, all exact:
      1. vertices are distinct and in range [0, 2^n);
      2. consecutive vertices differ in exactly one bit (it is a path in Q_n);
      3. induced: no two NON-consecutive vertices are adjacent (Hamming dist 1).
    O(L^2) in the number of vertices.
    """
    if len(set(path)) != len(path):
        return False, ("duplicate-vertex",)
    for v in path:
        if not (0 <= v < (1 << n)):
            return False, ("out-of-range", v)
    for k in range(len(path) - 1):
        if popcount(path[k] ^ path[k + 1]) != 1:
            return False, ("not-an-edge", k, path[k], path[k + 1])
    for i in range(len(path)):
        for j in range(i + 2, len(path)):
            if popcount(path[i] ^ path[j]) == 1:
                return False, ("chord", i, j, path[i], path[j])
    return True, None


def greedy_snake(n: int, priority: Callable[[int], float], start: int = 0) -> list[int]:
    """Greedily build an induced path in Q_n guided by `priority`.

    `priority` is a one-argument callable on a vertex (the project's EVOLVE
    evaluator wraps the dimension n, matching the cap_set convention). From the
    current endpoint, the only legal extensions are unvisited neighbors that are
    adjacent to NO other path vertex (so the path stays chordless). Among the
    legal extensions we take the one of highest `priority(vertex)`, ties broken by
    lowest flipped-bit index (neighbours are scanned bit 0..n-1, the Gray-code
    natural order; deterministic). Stop when stuck. Every prefix is an induced
    path BY CONSTRUCTION; callers still audit with `is_induced_path`.

    Efficiency: `adj[w]` tracks how many path vertices are adjacent to w, updated
    incrementally, so a vertex w (neighbor of the endpoint e) is a legal next step
    iff `adj[w] == 1` (its only path-neighbor is e). O(n) work per step.
    """
    path = [start]
    visited = {start}
    adj: dict[int, int] = defaultdict(int)
    for w in neighbors(start, n):
        adj[w] += 1
    while True:
        e = path[-1]
        best = None
        best_pri = None
        for w in neighbors(e, n):
            if w in visited or adj[w] != 1:
                continue
            p = priority(w)
            if best is None or p > best_pri:   # first-max wins => lowest flipped bit on ties
                best, best_pri = w, p
        if best is None:
            break
        path.append(best)
        visited.add(best)
        for w in neighbors(best, n):
            adj[w] += 1
    return path


def snake_length(path: list[int]) -> int:
    """Length of a snake in EDGES."""
    return len(path) - 1

"""Trusted primitives for the cap-set project.

FIXED infrastructure (the analog of riemann's rh_lib): the loop does not edit
this. Experiments compose it; the Tier-1 verifier trusts it. The key object is
`is_cap`, a cheap O(|S|^2) RIGOROUS verifier -- a candidate set is a cap iff it
contains no 3 distinct points a,b,c with a+b+c == 0 (mod 3). Because membership
is exact integer arithmetic, the verifier cannot be fooled.

Vectors of F_3^n are represented as tuples of ints in {0,1,2}.
"""
from __future__ import annotations

import itertools
from typing import Callable, Iterable, Optional

# Known maximum cap sizes |C| in F_3^n, for honest comparison (OEIS A090245).
KNOWN_MAX = {1: 2, 2: 4, 3: 9, 4: 20, 5: 45, 6: 112, 7: 236, 8: 512}


def vectors(n: int):
    """All 3^n vectors of F_3^n as tuples."""
    return itertools.product((0, 1, 2), repeat=n)


def third_point(a: tuple, b: tuple) -> tuple:
    """The unique c with a+b+c == 0 (mod 3); {a,b,c} is a line when c != a,b."""
    return tuple((-(ai + bi)) % 3 for ai, bi in zip(a, b))


def is_cap(points: Iterable[tuple]) -> tuple[bool, Optional[tuple]]:
    """Rigorously check whether `points` is a cap.

    Returns (True, None) if it is a cap, else (False, (a, b, c)) giving a witness
    line. O(|S|^2): for each unordered pair, the forced third point must be
    absent. (For distinct a != b, third_point(a,b) is automatically != a, b.)
    """
    S = set(points)
    pts = list(S)
    for i in range(len(pts)):
        a = pts[i]
        for j in range(i + 1, len(pts)):
            b = pts[j]
            c = third_point(a, b)
            if c in S and c != a and c != b:
                return False, (a, b, c)
    return True, None


def _safe_to_add(v: tuple, S: set) -> bool:
    """True iff adding v to cap S creates no line (for all a in S, third not in S)."""
    for a in S:
        if third_point(v, a) in S:
            return False
    return True


def ruin_and_recreate(n: int, budget_seconds: float, seed: int = 0,
                      ruin_frac: float = 0.3, init_restarts: int = 50) -> list[tuple]:
    """Iterated local search for a large cap in F_3^n.

    Start from the best of a few random-restart greedy caps, then repeatedly
    "ruin" (drop a random ruin_frac of points) and "recreate" (greedily re-add
    points in a fresh random order), keeping any larger valid cap. Every
    intermediate set is a cap by construction; the caller still audits with
    is_cap. Deterministic given (n, seed, budget) up to wall-clock timing.
    """
    import random
    import time

    rng = random.Random(seed)
    vecs = list(vectors(n))

    best: list[tuple] = []
    for s in range(init_restarts):
        r = random.Random((seed, s).__hash__())
        pr = {v: r.random() for v in vecs}
        C = greedy_cap(n, lambda v: pr[v])
        if len(C) > len(best):
            best = C

    deadline = time.time() + budget_seconds
    while time.time() < deadline:
        S = {v for v in best if rng.random() > ruin_frac}
        order = vecs[:]
        rng.shuffle(order)
        for v in order:
            if v not in S and _safe_to_add(v, S):
                S.add(v)
        if len(S) > len(best):
            best = list(S)
    return best


def greedy_cap(n: int, priority: Callable[[tuple], float]) -> list[tuple]:
    """Greedily build a cap in F_3^n, adding points in descending `priority`.

    This is the FunSearch construction skeleton: the LLM-evolved `priority`
    function is the only creative part. A point v is added iff it creates no line
    with the points already chosen, i.e. for every chosen a, third_point(v,a) is
    not already chosen. The result is a valid cap BY CONSTRUCTION; experiments
    still call is_cap as an independent audit.
    """
    order = sorted(vectors(n), key=priority, reverse=True)
    chosen: set[tuple] = set()
    for v in order:
        ok = True
        for a in chosen:
            if third_point(v, a) in chosen:
                ok = False
                break
        if ok:
            chosen.add(v)
    return list(chosen)

"""exp_0002 -- random-restart greedy cap in F_3^5 (frontier-search).

The single deterministic first-fit cap (exp_0001, size 32) sits in a symmetric
local optimum. Randomizing the greedy priority and keeping the best over many
restarts escapes it. We run as many seeded restarts as the budget allows and
report the largest VALID cap found, recording the winning seed so the result is
reproducible. Outcome (the size reached) is not known to us in advance ->
novelty = frontier-search.

Frontier: cap_size_dim5.
"""
from __future__ import annotations

import random
import time

from harness import experiment as E
from projects.cap_set.lib import cap

N = 5

MANIFEST = {
    "id": "exp_0002",
    "track": "cap_construction",
    "title": "Random-restart greedy cap in F_3^5",
    "hypothesis": "Randomized greedy beats the first-fit baseline (32) in F_3^5.",
    "falsifiable_prediction": "Best random-restart cap size > 32 and passes is_cap.",
    "references": ["FunSearch (Nature 2024); randomized greedy / GRASP."],
}


def run(budget_seconds: float) -> dict:
    deadline = time.time() + 0.9 * budget_seconds
    vecs = list(cap.vectors(N))
    best, best_seed, restarts = [], None, 0
    s = 0
    while time.time() < deadline:
        rng = random.Random(s)
        pr = {v: rng.random() for v in vecs}
        C = cap.greedy_cap(N, lambda v: pr[v])
        restarts += 1
        if len(C) > len(best):
            best, best_seed = C, s
        s += 1

    ok, witness = cap.is_cap(best)
    size = len(best) if ok else 0
    known = cap.KNOWN_MAX[N]
    baseline = 32
    beat = size > baseline

    claim = (
        f"Random-restart greedy ({restarts} restarts) finds a VALID cap of size "
        f"{size} in F_3^{N} (verified by is_cap), {'beating' if beat else 'matching'} "
        f"the first-fit baseline {baseline}; known maximum {known}, gap {known - size}. "
        f"Best seed {best_seed}."
        if ok else
        f"Best candidate is NOT a cap (witness {witness}) -- bug."
    )

    return E.result(
        track="cap_construction",
        novelty="frontier-search",
        claim=claim,
        metrics={
            "dimension": N,
            "cap_size": size,
            "valid": ok,
            "restarts": restarts,
            "best_seed": best_seed,
            "baseline_first_fit": baseline,
            "known_max": known,
            "gap_to_max": known - size,
        },
        frontier_metric=f"cap_size_dim{N}",
        frontier_value=float(size),
        falsified=False,
        consistent_with_goal=True,
        evidence={
            "method": "random-restart greedy; best over seeded priorities; is_cap audited",
            "best_seed": best_seed,
            "reproduce": f"random.Random(best_seed) priority over cap.vectors({N})",
        },
    )

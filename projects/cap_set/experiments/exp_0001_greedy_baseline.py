"""exp_0001 -- first-fit greedy cap in F_3^5 (baseline).

Establishes a baseline for the cap_construction frontier in dimension 5 using the
trivial constant priority (first-fit lexicographic order). The result is a valid
cap by construction; we audit it with cap.is_cap and report its size against the
known maximum (45). This is a reproduction (a trivial baseline), here only to set
the bar that later experiments must beat.

Frontier: cap_size_dim5.
"""
from __future__ import annotations

from harness import experiment as E
from projects.cap_set.lib import cap

N = 5

MANIFEST = {
    "id": "exp_0001",
    "track": "cap_construction",
    "title": "First-fit greedy cap in F_3^5 (baseline)",
    "hypothesis": "Constant-priority greedy yields a valid cap; size sets a baseline.",
    "falsifiable_prediction": "cap.is_cap accepts the constructed set.",
    "references": ["FunSearch (Nature 2024); cap set problem."],
}


def run(budget_seconds: float) -> dict:
    C = cap.greedy_cap(N, lambda v: 0)        # first-fit / lexicographic
    ok, witness = cap.is_cap(C)
    size = len(C) if ok else 0
    known = cap.KNOWN_MAX[N]

    claim = (
        f"First-fit greedy builds a VALID cap of size {size} in F_3^{N} "
        f"(verified by is_cap; known maximum {known}, gap {known - size}). Baseline."
        if ok else
        f"Constructed set is NOT a cap (witness {witness}) -- construction bug."
    )

    return E.result(
        track="cap_construction",
        novelty="reproduction",
        claim=claim,
        metrics={
            "dimension": N,
            "cap_size": size,
            "valid": ok,
            "known_max": known,
            "gap_to_max": known - size,
        },
        frontier_metric=f"cap_size_dim{N}",
        frontier_value=float(size),
        falsified=False,
        consistent_with_goal=True,
        evidence={
            "method": "greedy_cap with constant priority (first-fit)",
            "verified_by": "cap.is_cap O(|S|^2)",
            "sample_points": C[:8],
        },
    )

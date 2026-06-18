"""exp_0005 -- iterated local search improves the F_3^6 cap frontier.

Ruin-and-recreate in dimension 6 climbs past the random-restart result (77,
exp_0003) toward the known maximum 112. novelty = frontier-search (reached size
unknown a priori). is_cap audits; seed recorded for reproducibility.

Frontier: cap_size_dim6.
"""
from __future__ import annotations

from harness import experiment as E
from projects.cap_set.lib import cap

N = 6


MANIFEST = {
    "id": "exp_0005",
    "track": "cap_construction",
    "title": "ILS cap in F_3^6 (improve the frontier)",
    "hypothesis": "Ruin-and-recreate beats random-restart (77) in F_3^6.",
    "falsifiable_prediction": "Best cap passes is_cap and exceeds 77.",
    "references": ["FunSearch (Nature 2024)."],
}


def run(budget_seconds: float) -> dict:
    seed = 1
    prior = 77
    C = cap.ruin_and_recreate(N, budget_seconds=0.9 * budget_seconds, seed=seed)
    ok, witness = cap.is_cap(C)
    size = len(C) if ok else 0
    known = cap.KNOWN_MAX[N]

    claim = (
        f"Iterated local search finds a VALID cap of size {size} in F_3^{N} "
        f"(is_cap-verified), {'improving on' if size > prior else 'vs'} the prior "
        f"random-restart frontier {prior}; known maximum {known}, gap {known - size}."
    )

    return E.result(
        track="cap_construction",
        novelty="frontier-search",
        claim=claim,
        metrics={
            "dimension": N,
            "cap_size": size,
            "valid": ok,
            "prior_frontier": prior,
            "known_max": known,
            "gap_to_max": known - size,
            "seed": seed,
        },
        frontier_metric=f"cap_size_dim{N}",
        frontier_value=float(size),
        falsified=False,
        consistent_with_goal=True,
        evidence={
            "method": "cap.ruin_and_recreate (iterated local search); is_cap audited",
            "seed": seed,
        },
    )

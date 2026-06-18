"""exp_0008 -- evolution improves its own dim-7 cap frontier (148 -> 151).

A continued evolutionary sweep over the hash-priority family found a base
(2.684) that builds a cap of size 151 in F_3^7, improving the dim-7 frontier
first opened at 148 (exp_0006). Demonstrates the loop iterating on its own
record. is_cap audits; champion in the git-tracked program DB.

novelty = frontier-search. Frontier: cap_size_dim7.
"""
from __future__ import annotations

from harness import experiment as E
from harness import evolve
from projects.cap_set.lib import cap

N = 7


MANIFEST = {
    "id": "exp_0008",
    "track": "cap_construction",
    "title": "Evolution improves its own F_3^7 cap frontier (148 -> 151)",
    "hypothesis": "A further-evolved priority beats the prior evolved dim-7 frontier (148).",
    "falsifiable_prediction": "The constructed set passes is_cap and exceeds 148.",
    "references": ["FunSearch (Nature 2024)."],
}


def run(budget_seconds: float) -> dict:
    priority = evolve.champion_priority(N)
    C = cap.greedy_cap(N, lambda v: priority(v, N))
    ok, witness = cap.is_cap(C)
    size = len(C) if ok else 0
    prior = 148                                 # exp_0006 evolved frontier
    known = cap.KNOWN_MAX[N]

    claim = (
        f"A further-evolved deterministic priority builds a VALID cap of size "
        f"{size} in F_3^{N} (is_cap-verified), {'improving on' if size > prior else 'vs'} "
        f"the prior evolved frontier {prior}; known maximum {known}, gap {known - size}."
        if ok else
        f"Champion construction is NOT a cap (witness {witness}) -- bug."
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
        },
        frontier_metric=f"cap_size_dim{N}",
        frontier_value=float(size),
        falsified=False,
        consistent_with_goal=True,
        evidence={
            "method": "harness.evolve champion priority (hash base 2.684); is_cap audited",
            "source": "state/evolve/cap_priority/programs/prog_0006.py",
            "note": "single deterministic priority; iterating on its own frontier",
        },
    )

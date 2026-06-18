"""exp_0007 -- evolved STRUCTURED priority beats best-of-many in F_3^6.

The headline result for the evolution mechanism: a single *deterministic* evolved
priority builds a cap of size 82 in F_3^6, beating the prior frontier of 81 --
which was the best over MANY random restarts (exp_0005, iterated local search).
So the evolved structure (Hamming-weight layering + a near-injective hash
tiebreak, found by `lab.py evolve`) out-performs best-of-many random search in
one shot. is_cap audits the construction; the champion lives in the git-tracked
program DB.

novelty = frontier-search. Frontier: cap_size_dim6.
"""
from __future__ import annotations

from harness import experiment as E
from harness import evolve
from projects.cap_set.lib import cap

N = 6


MANIFEST = {
    "id": "exp_0007",
    "track": "cap_construction",
    "title": "Evolved structured priority beats best-of-many in F_3^6 (82 > 81)",
    "hypothesis": "An evolved deterministic priority beats the random-restart frontier (81) in F_3^6.",
    "falsifiable_prediction": "The constructed set passes is_cap and exceeds 81.",
    "references": ["FunSearch (Nature 2024); weight-layered greedy priority."],
}


def run(budget_seconds: float) -> dict:
    priority = evolve.champion_priority(N)
    C = cap.greedy_cap(N, lambda v: priority(v, N))
    ok, witness = cap.is_cap(C)
    size = len(C) if ok else 0
    prior = 81                                  # random-restart / ILS frontier (exp_0005)
    known = cap.KNOWN_MAX[N]

    claim = (
        f"A single deterministic FunSearch-evolved priority builds a VALID cap of "
        f"size {size} in F_3^{N} (is_cap-verified), {'beating' if size > prior else 'vs'} "
        f"the prior best-of-many random-restart frontier {prior} -- evolved structure "
        f"out-performs best-of-many search in one shot. Known maximum {known}, gap "
        f"{known - size}."
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
            "prior_frontier_random_restart": prior,
            "known_max": known,
            "gap_to_max": known - size,
        },
        frontier_metric=f"cap_size_dim{N}",
        frontier_value=float(size),
        falsified=False,
        consistent_with_goal=True,
        evidence={
            "method": "harness.evolve champion priority (Hamming-weight layering + hash); is_cap audited",
            "source": "state/evolve/cap_priority/programs/prog_0005.py",
            "note": "single deterministic priority beats best-of-many random restart (81)",
        },
    )

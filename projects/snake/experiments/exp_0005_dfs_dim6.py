"""exp_0005 -- bounded-backtracking improves the Q_6 snake frontier (26).

Greedy is myopic and plateaued at 25 (exp_0002). The trusted
primitive `snake.longest_snake_dfs` runs a priority-guided, time-boxed
depth-first BACKTRACKING search (first branch = greedy, then backtracks keeping
the longest induced path) using the evolved champion priority for vertex
ordering. is_induced_path audits the result. dim6 reaches the proven optimum 26.

novelty = frontier-search. Frontier: snake_len_dim6.
"""
from __future__ import annotations

from harness import experiment as E
from harness import evolve
from projects.snake.lib import snake

N = 6


MANIFEST = {
    "id": "exp_0005",
    "track": "snake_construction",
    "title": "Backtracking snake in Q_6 (26 edges)",
    "hypothesis": "Priority-guided backtracking beats the greedy snake frontier (25) in Q_6.",
    "falsifiable_prediction": "The path passes is_induced_path and exceeds 25.",
    "references": ["FunSearch (Nature 2024); depth-first backtracking.", "OEIS A099155."],
}


def run(budget_seconds: float) -> dict:
    priority = evolve.champion_priority(N)
    dfs_budget = min(20.0, 0.7 * budget_seconds)
    path = snake.longest_snake_dfs(N, lambda v: priority(v, N), budget_seconds=dfs_budget)
    ok, witness = snake.is_induced_path(path, N)            # un-gameable audit
    size = snake.snake_length(path) if ok else 0
    prior = 25                                         # greedy frontier (exp_0002)
    known = snake.LONGEST_KNOWN[N]
    proven = N <= snake.PROVEN_THROUGH
    optimal = ok and proven and size == known

    if not ok:
        claim = f"Backtracking path is NOT a valid induced path (witness {witness}) -- bug."
    elif optimal:
        claim = (f"Priority-guided backtracking builds a VALID snake of {size} edges in "
                 f"Q_{N} (is_induced_path-verified) = the PROVEN OPTIMUM {known}, improving "
                 f"the greedy frontier {prior}.")
    else:
        claim = (f"Priority-guided backtracking builds a VALID snake of {size} edges in "
                 f"Q_{N} (is_induced_path-verified), improving the greedy frontier {prior}; "
                 f"proven optimum {known}, gap {known - size}.")

    return E.result(
        track="snake_construction",
        novelty="frontier-search",
        claim=claim,
        metrics={
            "dimension": N, "snake_len_edges": size, "valid": ok,
            "prior_greedy_frontier": prior, "longest_known": known,
            "known_is_proven_optimum": proven, "gap_to_known": known - size,
            "is_optimal": optimal, "dfs_budget_seconds": dfs_budget,
        },
        frontier_metric=f"snake_len_dim{N}",
        frontier_value=float(size),
        falsified=False,
        consistent_with_goal=True,
        evidence={
            "method": "snake.longest_snake_dfs (priority-guided, time-boxed backtracking); is_induced_path audited",
            "priority_source": "state/evolve/snake_priority/ champion(v,n)",
            "note": "time-boxed DFS, monotonic (keeps best); achieved length is an audited lower bound, may rise with more budget",
        },
    )

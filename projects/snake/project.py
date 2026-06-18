"""Project descriptor: snake-in-the-box (longest induced path in Q_n).

The snake-in-the-box problem asks for the longest induced (chordless) path in the
n-dimensional hypercube graph Q_n. Exact maxima are known only through n=8; for
n>=9 the records are best-known lower bounds and have been largely untouched
since the 2000s -- a stale, under-attacked arena where a verifier-gated loop has
a realistic shot. The verifier (`lib/snake.is_induced_path`) is a cheap, exact,
un-gameable O(L^2) check; the evolvable object is a `priority` function over
hypercube vertices used by a greedy path-builder (the FunSearch pattern).

Longest snake (edges): n: 5 6 7 8  ->  13 26 50 98  (proven optima).
"""

NAME = "snake"

CONJECTURE = (
    "Find long snakes (induced/chordless paths) in the hypercube Q_n. "
    "Frontier: snake length (edges) per dimension; honest target = the known "
    "optima for n<=8 and best-known lower bounds for n>=9."
)

TRACKS = {
    "snake_construction": "Construct a long induced path (snake) in Q_n via a greedy priority; frontier = snake length (edges) in dimension n.",
    "coil_construction": "Construct a long induced CYCLE (coil) in Q_n; frontier = coil length in dimension n.",
}


# --------------------------------------------------------------------------- #
# FunSearch evolution spec (consumed by harness/evolve.py via `lab.py evolve`).
# Evolve priority(v, n) -> float over hypercube vertices; the greedy builder
# extends the snake by the highest-priority legal vertex. The evaluator runs the
# build across a cluster of dimensions and audits EVERY snake with the rigorous
# is_induced_path, so length can only be earned by a genuine chordless path.
# --------------------------------------------------------------------------- #
EVOLVE_CLUSTER = [5, 6, 7, 8]

EVOLVE_SEED = '''\
def priority(v, n):
    """Trivial seed program: constant priority => first-fit greedy snake. Beat me.

    v is a hypercube vertex (an int in [0, 2**n), an n-bit string); n is the
    dimension. Return a float; the greedy builder extends the current snake by
    the legal neighbour (unvisited, keeps the path chordless) of HIGHEST priority.
    """
    return 0.0
'''


def _evolve_evaluate(priority):
    """Rigorously score a candidate `priority` across the cluster of dimensions.

    Returns {"valid", "scores": {dim: snake_length_edges}, "fitness", "audit"}.
    Any exception from the candidate, or any path that fails is_induced_path,
    makes the program invalid (length 0 for that dim).
    """
    from projects.snake.lib import snake

    scores: dict[int, int] = {}
    valid = True
    audit = None
    for n in EVOLVE_CLUSTER:
        try:
            path = snake.greedy_snake(n, lambda v: priority(v, n))
            ok, witness = snake.is_induced_path(path, n)
        except Exception as e:
            valid = False
            audit = {"dim": n, "error": repr(e)}
            scores[n] = 0
            continue
        if not ok:
            valid = False
            audit = {"dim": n, "witness": witness}
            scores[n] = 0
        else:
            scores[n] = snake.snake_length(path)
    return {
        "valid": valid,
        "scores": scores,
        "fitness": float(sum(scores.values())),
        "audit": audit,
    }


EVOLVE = {
    "name": "snake_priority",
    "signature": "def priority(v, n) -> float   # v: hypercube vertex int in [0,2**n), n: dimension",
    "entry": "priority",
    "evaluate": _evolve_evaluate,
    "seed": EVOLVE_SEED,
    "islands": 4,
    "cluster": EVOLVE_CLUSTER,
}

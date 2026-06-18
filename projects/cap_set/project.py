"""Project descriptor: cap sets in F_3^n.

A cap set is a subset of F_3^n containing no 3 distinct points on a line (no
a,b,c distinct with a+b+c = 0 mod 3) -- equivalently, no 3-term arithmetic
progression. The goal is to find LARGE caps. This is the flagship FunSearch
problem: an LLM evolves a `priority` function over F_3^n vectors used by a greedy
constructor, and a cheap, rigorous verifier scores the result by cap size.

Known maximum cap sizes (for honest comparison):
  n:  1  2  3   4   5    6    7    8
  |C|:2  4  9  20  45  112  236  512
"""

NAME = "cap_set"

CONJECTURE = (
    "Find large cap sets in F_3^n (no 3 distinct collinear points). "
    "Frontier: cap size per dimension; honest target = the known maxima."
)

TRACKS = {
    "cap_construction": "Construct a large cap in F_3^n via a greedy priority function; frontier = cap size in dimension n.",
    "cap_lower_bound": "Improve the asymptotic cap-set capacity lower bound via a product/recursive construction.",
}


# --------------------------------------------------------------------------- #
# FunSearch evolution spec (consumed by harness/evolve.py via `lab.py evolve`).
#
# The agent evolves a single function, `priority(v, n) -> float`, used by the
# greedy constructor to order F_3^n vectors. The evaluator runs that greedy
# build across a CLUSTER of dimensions and audits EVERY result with is_cap, so
# fitness can only be earned by actually building larger valid caps. This is the
# canonical FunSearch setup (Nature 2024): evolve the priority, score rigorously.
# --------------------------------------------------------------------------- #
EVOLVE_CLUSTER = [4, 5, 6, 7]

EVOLVE_SEED = '''\
def priority(v, n):
    """Trivial seed program: constant priority => first-fit greedy. Beat me.

    v is a tuple in F_3^n (entries in {0,1,2}); n is the dimension. Return a
    float; the greedy constructor adds vectors in DESCENDING priority, skipping
    any that would complete a line with the points already chosen.
    """
    return 0.0
'''


def _evolve_evaluate(priority):
    """Rigorously score a candidate `priority` across the cluster of dimensions.

    Returns {"valid", "scores": {dim: cap_size}, "fitness", "audit"}. Any
    exception from the candidate, or any construction that fails is_cap, makes
    the program invalid (fitness still reported for the dims that did build).
    """
    from projects.cap_set.lib import cap

    scores: dict[int, int] = {}
    valid = True
    audit = None
    for n in EVOLVE_CLUSTER:
        try:
            C = cap.greedy_cap(n, lambda v: priority(v, n))
            ok, witness = cap.is_cap(C)
        except Exception as e:  # a buggy candidate must not crash the loop
            valid = False
            audit = {"dim": n, "error": repr(e)}
            scores[n] = 0
            continue
        if not ok:
            valid = False
            audit = {"dim": n, "witness": witness}
            scores[n] = 0
        else:
            scores[n] = len(C)
    return {
        "valid": valid,
        "scores": scores,
        "fitness": float(sum(scores.values())),
        "audit": audit,
    }


EVOLVE = {
    "name": "cap_priority",
    "signature": "def priority(v, n) -> float   # v: tuple in F_3^n, n: dimension",
    "entry": "priority",
    "evaluate": _evolve_evaluate,
    "seed": EVOLVE_SEED,
    "islands": 4,
    "cluster": EVOLVE_CLUSTER,
}

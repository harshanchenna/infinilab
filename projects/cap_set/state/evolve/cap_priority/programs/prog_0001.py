import math


def priority(v, n):
    """Evolved symmetry-breaking hash priority for greedy cap construction.

    A near-injective deterministic ordering: interpret v as a base-3.49 positional
    hash and take sin(.). Fine structure (few ties) lets greedy explore a good
    order; the multiplier 3.49 was found by evolutionary sweep over the cluster.
    Reproducible: the multiplier is an exact literal.
    """
    h = sum((x + 1) * (3.49 ** (i + 1)) for i, x in enumerate(v))
    return math.sin(h)

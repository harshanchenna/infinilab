import math


def priority(v, n):
    """Evolved symmetry-breaking hash priority for greedy cap construction.

    A near-injective deterministic ordering: interpret v as a base-2.59 positional
    hash and take sin(.). Fine structure (few ties) lets greedy explore a good
    order; the multiplier 2.59 was found by evolutionary sweep over the cluster.
    Reproducible: the multiplier is an exact literal.
    """
    h = sum((x + 1) * (2.59 ** (i + 1)) for i, x in enumerate(v))
    return math.sin(h)

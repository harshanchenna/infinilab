import math


def priority(v, n):
    """Evolved structured priority (weight-layer, light coeff) -- champion at dim 5.

    Hamming-weight layering with a small coefficient under a near-injective hash
    tiebreak; builds a valid cap of size 40 in F_3^5, beating the random-restart
    frontier (39). Exact literals => reproducible.
    """
    wt = sum(1 for x in v if x)
    h = math.sin(sum((x + 1) * (2.6466 ** (i + 1)) for i, x in enumerate(v)))
    return -1.0 * wt + h

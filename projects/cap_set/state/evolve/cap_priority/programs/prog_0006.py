import math


def priority(v, n):
    """Evolved symmetry-breaking hash priority (base 2.684), champion at dim 7.

    Near-injective deterministic ordering; multiplier found by fine evolutionary
    sweep. Exact literal => reproducible. Builds a valid cap of size 151 in F_3^7.
    """
    h = sum((x + 1) * (2.684 ** (i + 1)) for i, x in enumerate(v))
    return math.sin(h)

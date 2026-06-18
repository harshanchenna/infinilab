import math


def priority(v, n):
    """Evolved phase-hash priority -- reaches the proven optimum snake (13) at dim5.

    A near-injective ordering by sin(m * Σ bit_i·(i+1)); the multiplier was found
    by evolutionary sweep. Exact literal => reproducible.
    """
    return math.sin(2.2208559756579547 * sum(((v >> i) & 1) * (i + 1) for i in range(n)))

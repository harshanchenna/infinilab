import math


def priority(v, n):
    """Evolved weight-layered priority (light coeff) -- snake 76 at dim8 (optimum 98).

    Order by Hamming weight with a small coefficient under a hash tiebreak. Exact
    literals => reproducible.
    """
    return -1.0 * bin(v).count('1') + math.sin(
        sum((((v >> i) & 1) + 1) * (2.5497311651835233 ** (i + 1)) for i in range(n)))

import math


def priority(v, n):
    """Evolved weight-layered priority -- snake 46 at dim7 (optimum 50).

    Order by descending Hamming weight (coeff -8) under a hash tiebreak. Exact
    literals => reproducible.
    """
    return -8.0 * bin(v).count('1') + math.sin(
        sum((((v >> i) & 1) + 1) * (2.8061098355380203 ** (i + 1)) for i in range(n)))

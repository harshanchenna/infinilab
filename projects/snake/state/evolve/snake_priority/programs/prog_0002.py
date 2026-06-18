import math


def priority(v, n):
    """Evolved parity-layered priority -- snake 25 at dim6 (optimum 26).

    Order primarily by hypercube parity (the bipartition colour) under a hash
    tiebreak. Exact literals => reproducible.
    """
    return 8.0 * (bin(v).count('1') % 2) + math.sin(
        sum((((v >> i) & 1) + 1) * (1.1762328731289924 ** (i + 1)) for i in range(n)))

def priority(v, n):
    """Trivial seed program: constant priority => first-fit greedy snake. Beat me.

    v is a hypercube vertex (an int in [0, 2**n), an n-bit string); n is the
    dimension. Return a float; the greedy builder extends the current snake by
    the legal neighbour (unvisited, keeps the path chordless) of HIGHEST priority.
    """
    return 0.0

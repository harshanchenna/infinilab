def priority(v, n):
    """Trivial seed program: constant priority => first-fit greedy. Beat me.

    v is a tuple in F_3^n (entries in {0,1,2}); n is the dimension. Return a
    float; the greedy constructor adds vectors in DESCENDING priority, skipping
    any that would complete a line with the points already chosen.
    """
    return 0.0

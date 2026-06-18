"""Project descriptor: cap sets in F_3^n.

A cap set is a subset of F_3^n containing no 3 distinct points on a line (no
a,b,c distinct with a+b+c = 0 mod 3) -- equivalently, no 3-term arithmetic
progression. The goal is to find LARGE caps. This is the flagship FunSearch
problem: an LLM evolves a `priority` function over F_3^n vectors used by a greedy
constructor, and a cheap, rigorous verifier scores the result by cap size.

Known maximum cap sizes (for honest comparison):
  n:  1  2  3   4   5    6    7    8
  |C|:2  4  9  20  45  112  236  512
"""

NAME = "cap_set"

CONJECTURE = (
    "Find large cap sets in F_3^n (no 3 distinct collinear points). "
    "Frontier: cap size per dimension; honest target = the known maxima."
)

TRACKS = {
    "cap_construction": "Construct a large cap in F_3^n via a greedy priority function; frontier = cap size in dimension n.",
    "cap_lower_bound": "Improve the asymptotic cap-set capacity lower bound via a product/recursive construction.",
}

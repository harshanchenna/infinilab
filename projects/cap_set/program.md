# program.md — cap sets in F_3^n

## Goal
Find LARGE cap sets in F_3^n (subsets with no 3 distinct collinear points, i.e.
no a,b,c with a+b+c = 0 mod 3). This is FunSearch's flagship problem. Progress is
measured by cap size per dimension; the honest target is the known maximum
(n: 2,4,9,20,45,112,236,512 for n=1..8).

## How progress is measured
- **Tier 1 (truth):** `projects/cap_set/lib/cap.py::is_cap` rigorously checks a
  candidate is a cap in O(|S|^2) -- pure integer arithmetic, un-gameable. Every
  experiment must produce a set that `is_cap` accepts; its size is the frontier.
- **Tier 2 (soundness):** the skeptic vets the claim (is the size the verified
  size? is novelty honest? is it gaming a per-dimension metric?).

Frontiers are keyed per dimension: `cap_construction::cap_size_dim<n>`.

## The method to evolve (FunSearch-style)
`cap.greedy_cap(n, priority)` builds a cap by adding points in descending
`priority` order, skipping any point that would complete a line. The ONLY
creative part is the `priority` function over F_3^n vectors. Baselines:
first-fit (constant priority) gives 16 (n=4), 32 (n=5); random-restart greedy
reaches 18, 38, ~75 (n=4,5,6). Beating those needs a cleverer priority.

## Rules
- Never edit `lib/`. Compose it. A new construction must pass `is_cap`.
- Claims entailed by the verified size. Don't claim a record you didn't reach;
  report distance to the known maximum honestly.
- Reproducible: if you use randomness, fix and record seeds in `evidence`.
- Respect the wall-clock budget; return the best cap found so far.

## Tracks
- `cap_construction` — a large cap in a specific dimension (frontier = size).
- `cap_lower_bound` — asymptotic capacity via product/recursive constructions.

## Current focus
Climb the per-dimension frontier in n=4..7 with better priority functions and
randomized search; then attempt a product construction for the asymptotic bound.

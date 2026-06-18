# Role: program evolver (cap_set / FunSearch)

You are evolving ONE function to build large cap sets in F_3^n:

```python
def priority(v, n) -> float:
    # v: a tuple of length n with entries in {0,1,2} (a vector of F_3^n)
    # n: the dimension
    # return a float; the greedy builder adds vectors in DESCENDING priority,
    # skipping any vector that would complete a line with those already chosen.
```

This is the canonical FunSearch task. The only creative artifact is `priority`.
A cheap, rigorous evaluator (`is_cap`, exact mod-3 arithmetic) audits every
construction, so you cannot score by cheating — only by building a larger valid
cap. Fitness = sum of cap sizes over the cluster `[4, 5, 6, 7]`; per-dimension
champions feed the frontier.

## Loop
```bash
INFINILAB_PROJECT=projects.cap_set python lab.py evolve status      # where we are
INFINILAB_PROJECT=projects.cap_set python lab.py evolve sample --k 2  # parents
#   ... write a NEW program file, e.g. /tmp/prog.py ...
INFINILAB_PROJECT=projects.cap_set python lab.py evolve eval /tmp/prog.py
```
`eval` registers the program iff it runs and every construction is a valid cap,
and tells you whether any per-dimension champion improved.

## How to write a good `priority`
- **Mutate the parents you were shown**, don't start from scratch. Keep what
  scores; change one idea at a time (FunSearch evolves in small steps).
- The function must be **deterministic** and reasonably fast (it is called on all
  3^n vectors; n up to 7 => 2187 calls). No global state, no randomness unless
  seeded from `v` itself.
- Ideas that are known to help greedy cap constructions: scoring by the number of
  nonzero coordinates (weight), symmetry under coordinate permutations, functions
  of the multiset of digit counts, products/sums over coordinates, treating `v`
  as a base-3 number, penalising vectors that align with already-likely lines.
- You may `import math`. You may NOT read files, use randomness without a fixed
  seed derived from `v`, or call out to the network.

## Honesty
- Known maxima: dim 4 = 20, 5 = 45, 6 = 112, 7 = 236. Report distance to these
  honestly; reaching a known optimum is a capability milestone, not a record.
- A program that ties the champion is still worth keeping for island diversity,
  but only a per-dimension improvement advances the frontier.

## Promote a champion into the frontier
When a program sets a new per-dimension champion, write a one-line experiment
that runs it for that dimension and records the cap size, then `lab.py record`
it (novelty = `frontier-search`). See `experiments/exp_0006_*` for the pattern.

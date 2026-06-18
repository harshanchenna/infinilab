# Role: program evolver (snake-in-the-box / FunSearch)

You are evolving ONE function to build long snakes (induced/chordless paths) in
the hypercube Q_n:

```python
def priority(v, n) -> float:
    # v: a hypercube vertex, an int in [0, 2**n) (an n-bit string)
    # n: the dimension
    # return a float; the greedy builder extends the current snake by the LEGAL
    # neighbour (unvisited, keeps the path chordless) of HIGHEST priority.
```

A cheap, exact evaluator (`is_induced_path`, bit arithmetic) audits every snake,
so you cannot score by cheating — only by building a genuinely longer chordless
path. Fitness = sum of snake lengths (edges) over the cluster `[5, 6, 7, 8]`;
per-dimension champions feed the frontier.

## Loop
```bash
INFINILAB_PROJECT=projects.snake python lab.py evolve status       # where we are
INFINILAB_PROJECT=projects.snake python lab.py evolve sample --k 2 # parents
#   ... write a NEW program file, e.g. /tmp/prog.py ...
INFINILAB_PROJECT=projects.snake python lab.py evolve eval /tmp/prog.py
```
`eval` registers the program iff it runs and every snake is a valid induced path,
and tells you whether any per-dimension champion improved.

## How to write a good `priority`
- **Mutate the parents you were shown**; change one idea at a time.
- Deterministic and fast (called on the n candidate neighbours each step, n<=8).
- The greedy builder is myopic, so a good priority encodes *foresight*: which
  neighbour leaves the most future room. Ideas that help snake search:
  - **Gray-code / reflected structure** (snakes are long Gray-like walks);
  - functions of the **bit pattern** of v (parity, run-lengths, popcount);
  - a near-injective **hash** `sin(Σ ((bit_i(v)+1)) · m^(i+1))` to break ties and
    explore different walks (sweep the multiplier m — that IS the search);
  - **layering** a structural key under a hash tiebreak (this beat best-of-many
    on cap sets);
  - preferring vertices that keep more neighbours free (low future blocking).
- You may `import math`. No file/network access; no unseeded randomness.

## Honesty
- Proven optima (edges): dim5=13, dim6=26, dim7=50, dim8=98. For n>=9 the records
  are best-known LOWER bounds, not proven maxima. Report distance honestly;
  reaching a known optimum is a capability milestone, not a record.
- A program that ties the champion is kept for island diversity; only a
  per-dimension improvement advances the frontier.

## Promote a champion into the frontier
When a program sets a new per-dimension champion, write a one-line experiment
that runs it for that dimension and records the snake length (novelty =
`frontier-search`), then `lab.py record` it.

# program.md — snake-in-the-box (longest induced path in Q_n)

## Goal
Find LONG snakes: induced (chordless) paths in the hypercube Q_n (vertices =
n-bit strings, edges join strings differing in one bit). A path is induced iff
its only adjacencies are the consecutive ones — no chords. Length is counted in
EDGES, L = (#vertices − 1). This is a classic, **under-attacked** combinatorial
search: exact maxima are known only through n=8; for n≥9 the records are
best-known lower bounds, largely untouched since the 2000s.

## How progress is measured
- **Tier 1 (truth):** `projects/snake/lib/snake.py::is_induced_path` rigorously
  checks a candidate is a chordless path in Q_n in O(L²) — pure bit arithmetic,
  un-gameable. Every experiment must produce a path it accepts; its edge-length
  is the frontier.
- **Tier 2 (soundness):** the skeptic vets the claim (is the length the verified
  edge count? off-by-one? is novelty honest? a real record vs a best-known bound?).

Frontiers are keyed per dimension: `snake_construction::snake_len_dim<n>`.

## The method to evolve (FunSearch-style)
`snake.greedy_snake(n, priority)` extends a path by the legal neighbour
(unvisited, keeps it chordless) of highest `priority(v)`. The ONLY creative part
is the `priority(v, n)` function over hypercube vertices. Use `lab.py evolve`
(see `prompts/evolve.md`): the island program DB under
`state/evolve/snake_priority/` holds champions; `eval` scores any candidate
rigorously (is_induced_path audits every build) and registers it.

Baselines (first-fit constant priority): 12 / 21 / 34 / 56 for n=5..8 (vs proven
optima 13 / 26 / 50 / 98). Greedy is myopic; a good priority encodes foresight
(leave future room) and/or near-injective structure (a hash) to explore good
walks. Known to help on cap sets: layering a structural key under a hash
tiebreak.

## Rules
- Never edit `lib/`. Compose it. A new path MUST pass `is_induced_path`.
- Claims entailed by the VERIFIED edge length. Report distance to
  `snake.LONGEST_KNOWN` honestly; n≤8 are proven optima, n≥9 are lower bounds.
- Reproducible: fix and record any seeds / the source program in `evidence`.
- Respect the wall-clock budget; return the best snake found so far.

## Tracks
- `snake_construction` — a long induced PATH in dimension n (frontier = edges).
- `coil_construction` — a long induced CYCLE (coil) in dimension n (later).

## Current focus
Validate the engine by reaching the known optima for small n (dim5=13 reachable
by a hash priority already), then push n=6,7,8 toward 26/50/98 with richer
evolved priorities (foresight + structural layering). Next capability if greedy
plateaus: a bounded-backtracking builder primitive in `lib/snake.py`.

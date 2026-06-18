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
creative part is the `priority(v, n)` function over F_3^n vectors. Use the real
evolution loop (`lab.py evolve`, see `prompts/evolve.md`): the island program DB
under `state/evolve/cap_priority/` holds champions; `eval` scores any candidate
rigorously (is_cap audits every build) and registers it.

**Key lesson (recorded):** smooth priorities with many ties collapse to first-fit
(16/32/64/128 over dims 4-7). What works is *fine, near-injective structure*. Two
families found so far: (a) a base-`m` positional **hash** `sin(Σ(v_i+1)·m^(i+1))`
that breaks symmetry, and (b) **weight-layering** — order by Hamming weight under
a hash tiebreak — which beats best-of-many random restart.

**Current evolved champions (dims 4-7): 20 / 40 / 82 / 151** (vs known maxima
20/45/112/236). dim4 is the proven optimum; dim5/6/7 each beat the prior
random-restart/ILS frontier with a single DETERMINISTIC evolved priority.

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
Close the remaining gaps to the known maxima (dim5 40->45, dim6 82->112, dim7
151->236) with richer evolved priorities — try multi-key layering (weight +
coordinate-pattern + hash), and consider letting the priority encode a small
amount of search. Then attempt a product/recursive construction for the
asymptotic `cap_lower_bound` track.

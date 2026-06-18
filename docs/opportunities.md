# Where infinilab can have an impact (research sprint synthesis)

A verifier-gated autoresearch loop (LLM proposes a candidate -> a cheap program
scores it rigorously -> keep-if-better) is strongest where a candidate solution
is **cheaply and rigorously checkable** and there's a **public record to beat**.
RH fails this (no cheap scalar; mostly reproduction). The sweet spot is
FunSearch/AlphaEvolve-style **construction & extremal problems**. Synthesis of a
multi-agent literature sprint (June 2026); all claims cited below.

## What LLM+evaluator loops have ALREADY done (proof the paradigm works)
- **FunSearch** (Nature 2024): cap set in F_3^8 496->512; asymptotic cap-set
  lower bound 2.2180->2.2202; better online bin-packing heuristics.
  <https://www.nature.com/articles/s41586-023-06924-6>
- **AlphaEvolve** (2025): 4x4 complex matrix mult 49->48 (beat Strassen);
  kissing number d=11 592->593; improved ~20% of 50+ open problems.
  <https://arxiv.org/abs/2506.13131>, <https://arxiv.org/abs/2511.02864> (Tao et al.)
- **Ramsey** (2026): AlphaEvolve improved 9 Ramsey lower bounds (e.g. R(4,19)
  213->219). <https://arxiv.org/abs/2603.09172>
- **Erdős minimum overlap**: upper bound improved 3x in 12 months by AI systems
  (AlphaEvolve 0.380924; Together AI / EinsteinArena 0.380870).
- **Kissing d=11**: 593 (AlphaEvolve) -> 604 (EinsteinArena, 2026).
- **Low-resource FunSearch** reimplementation, "no HPC required" (Ellenberg et
  al. 2025): <https://arxiv.org/abs/2503.11061> -- single-machine is viable.

## Ranked targets for infinilab (cheap rigorous verifier + live record table)
1. **Cap sets in F_3^n** (chosen first project). Verifier: O(|S|^2) -- no 3
   distinct vectors sum to 0. Maps perfectly onto "evolve a priority function for
   a greedy construction" (FunSearch's flagship). Small-n optima known
   (n: 2,4,9,20,45,112,236,512) so progress is measurable and honest.
2. **Erdős minimum overlap** (★★★★★). Verifier: O(G log G) overlap integral of a
   G-step function. Lowest barrier; most active AI-competition arena.
   <https://en.wikipedia.org/wiki/Minimum_overlap_problem>
3. **Kissing numbers** (★★★★★). Verifier: O(K^2 d) pairwise dot products <= 1/2.
   Proven arena for LLM loops. <https://cohn.mit.edu/kissing-numbers/>
4. **Snake-in-the-box** (★★★★). Verifier: O(L) induced-path check on the
   hypercube. No records broken since ~2016 -> ripe. OEIS A000937.
5. **Low-autocorrelation binary sequences (LABS)** (★★★★). Verifier: O(n^2) merit
   factor F = n^2/(2 sum C_k^2). Real-valued signal; frontier n=100-300.
6. **Linear codes [n,k,d]** (Grassl tables) / **van der Waerden & Schur lower
   bounds** / **no-three-in-line**: all cheap exact verifiers with public tables.

## Why cap sets first
It is the canonical FunSearch problem, the verifier is ~10 lines and rigorous,
the "function to evolve" (a priority over F_3^n vectors used by a greedy builder)
fits our experiment contract exactly, and known optima for small n let us report
honest progress (and honest distance from records) rather than reproduction. It
is the cleanest demonstration that the project-agnostic engine works on a domain
with a genuine, un-gameable, FunSearch-style verifier.

## Honest ceiling
Beating a *live* world record (kissing, Erdős overlap) is contested by
well-resourced teams; a modest single-machine loop more realistically (a)
re-derives known optima, (b) advances its own per-instance frontier, and
(c) occasionally improves a stale, under-attacked record (snake-in-the-box,
specific LABS/code-table entries). We aim there and report distance-to-record
honestly.

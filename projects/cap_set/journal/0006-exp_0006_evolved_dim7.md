# Iteration 0006 -- Evolved priority opens the F_3^7 cap frontier

- **module**: `projects.cap_set.experiments.exp_0006_evolved_dim7`
- **track**: `cap_construction`  |  **novelty**: frontier-search
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: cap_size_dim7 = 148.0
- **skeptic**: sound -- is_cap-audited valid cap; opens dim7 above first-fit 128; novelty frontier-search correct; claim explicitly not best-of-many, gap-to-max 88 stated -- no overclaim
- **elapsed**: 0.2s

## Hypothesis
The FunSearch-evolved champion priority builds a large valid cap in F_3^7.

## Claim (entailed by the numbers)
A FunSearch-evolved deterministic priority builds a VALID cap of size 148 in F_3^7 (is_cap-verified), opening the dim-7 frontier (first-fit baseline 128); known maximum 236, gap 88. The candidate was selected by a rigorous evaluator (is_cap audits every construction), demonstrating the evolution mechanism end-to-end.

## Metrics
```json
{
  "dimension": 7,
  "cap_size": 148,
  "valid": true,
  "baseline_first_fit": 128,
  "known_max": 236,
  "gap_to_max": 88
}
```

## Evidence
```json
{
  "method": "harness.evolve champion priority(v,n); greedy_cap; is_cap audited",
  "source": "state/evolve/cap_priority/ (git-tracked program DB)",
  "note": "single deterministic priority; not best-of-many random restart"
}
```

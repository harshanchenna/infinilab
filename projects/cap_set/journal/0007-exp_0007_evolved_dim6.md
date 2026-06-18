# Iteration 0007 -- Evolved structured priority beats best-of-many in F_3^6 (82 > 81)

- **module**: `projects.cap_set.experiments.exp_0007_evolved_dim6`
- **track**: `cap_construction`  |  **novelty**: frontier-search
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: cap_size_dim6 = 82.0
- **skeptic**: sound -- is_cap-audited cap 82 > recorded ILS frontier 81; gap-to-max 30 stated; structured evolved priority beats best-of-many honestly
- **elapsed**: 0.1s

## Hypothesis
An evolved deterministic priority beats the random-restart frontier (81) in F_3^6.

## Claim (entailed by the numbers)
A single deterministic FunSearch-evolved priority builds a VALID cap of size 82 in F_3^6 (is_cap-verified), beating the prior best-of-many random-restart frontier 81 -- evolved structure out-performs best-of-many search in one shot. Known maximum 112, gap 30.

## Metrics
```json
{
  "dimension": 6,
  "cap_size": 82,
  "valid": true,
  "prior_frontier_random_restart": 81,
  "known_max": 112,
  "gap_to_max": 30
}
```

## Evidence
```json
{
  "method": "harness.evolve champion priority (Hamming-weight layering + hash); is_cap audited",
  "source": "state/evolve/cap_priority/programs/prog_0005.py",
  "note": "single deterministic priority beats best-of-many random restart (81)"
}
```

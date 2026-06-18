# Iteration 0002 -- Random-restart greedy cap in F_3^5

- **module**: `projects.cap_set.experiments.exp_0002_random_restart`
- **track**: `cap_construction`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: cap_size_dim5 = 39.0
- **skeptic**: sound -- Claim is entailed by the numbers: valid size-39 cap, correctly beats baseline 32, honestly reports gap 6 to known max 45 without claiming a record. Frontier-search novelty fits (outcome unknown a priori); frontier_value backed by a real is_cap-verified construction. Integer combinatorics, no numerical-precision risk. Seed makes it reproducible.
- **elapsed**: 54.1s

## Hypothesis
Randomized greedy beats the first-fit baseline (32) in F_3^5.

## Claim (entailed by the numbers)
Random-restart greedy (26954 restarts) finds a VALID cap of size 39 in F_3^5 (verified by is_cap), beating the first-fit baseline 32; known maximum 45, gap 6. Best seed 874.

## Metrics
```json
{
  "dimension": 5,
  "cap_size": 39,
  "valid": true,
  "restarts": 26954,
  "best_seed": 874,
  "baseline_first_fit": 32,
  "known_max": 45,
  "gap_to_max": 6
}
```

## Evidence
```json
{
  "method": "random-restart greedy; best over seeded priorities; is_cap audited",
  "best_seed": 874,
  "reproduce": "random.Random(best_seed) priority over cap.vectors(5)"
}
```

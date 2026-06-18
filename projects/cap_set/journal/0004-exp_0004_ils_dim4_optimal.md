# Iteration 0004 -- ILS reaches the optimal cap (size 20) in F_3^4

- **module**: `projects.cap_set.experiments.exp_0004_ils_dim4_optimal`
- **track**: `cap_construction`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: cap_size_dim4 = 20.0
- **skeptic**: n/a
- **elapsed**: 21.4s

## Hypothesis
Ruin-and-recreate finds a size-20 (optimal) cap in F_3^4.

## Claim (entailed by the numbers)
Iterated local search finds a VALID cap of size 20 in F_3^4 (is_cap-verified) = the PROVEN MAXIMUM 20: the loop reaches the optimum where one is known.

## Metrics
```json
{
  "dimension": 4,
  "cap_size": 20,
  "valid": true,
  "known_max": 20,
  "gap_to_max": 0,
  "is_optimal": true,
  "seed": 1
}
```

## Evidence
```json
{
  "method": "cap.ruin_and_recreate (iterated local search); is_cap audited",
  "seed": 1,
  "optimal": true
}
```

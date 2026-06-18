# Iteration 0001 -- First-fit greedy cap in F_3^5 (baseline)

- **module**: `projects.cap_set.experiments.exp_0001_greedy_baseline`
- **track**: `cap_construction`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: cap_size_dim5 = 32.0
- **skeptic**: sound -- Honest baseline reproduction. Claim asserts only a valid size-32 cap verified by is_cap, explicitly notes gap 13 to known max 45, and labels itself a baseline. Novelty correctly 'reproduction'; frontier_value matches cap_size. No overclaiming, no falsification, no metric gaming.
- **elapsed**: 0.3s

## Hypothesis
Constant-priority greedy yields a valid cap; size sets a baseline.

## Claim (entailed by the numbers)
First-fit greedy builds a VALID cap of size 32 in F_3^5 (verified by is_cap; known maximum 45, gap 13). Baseline.

## Metrics
```json
{
  "dimension": 5,
  "cap_size": 32,
  "valid": true,
  "known_max": 45,
  "gap_to_max": 13
}
```

## Evidence
```json
{
  "method": "greedy_cap with constant priority (first-fit)",
  "verified_by": "cap.is_cap O(|S|^2)",
  "sample_points": [
    [
      1,
      1,
      1,
      0,
      0
    ],
    [
      0,
      1,
      0,
      0,
      1
    ],
    [
      0,
      0,
      1,
      0,
      0
    ],
    [
      1,
      0,
      1,
      1,
      0
    ],
    [
      0,
      0,
      0,
      0,
      0
    ],
    [
      0,
      1,
      1,
      1,
      1
    ],
    [
      1,
      1,
      1,
      1,
      1
    ],
    [
      1,
      0,
      0,
      1,
      0
    ]
  ]
}
```

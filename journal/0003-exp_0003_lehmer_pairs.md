# Iteration 0003 -- Smallest normalized gap between consecutive zeta zeros

- **module**: `experiments.exp_0003_lehmer_pairs`
- **track**: `lehmer_pairs`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: n_zeros_scanned = 300.0
- **skeptic**: sound -- Conservative claim: 0.29 min gap is not even an anomalously close pair, no disproof asserted, RH-consistency correctly stated. DPS=25 ample for heights ~415; K=300 frontier honestly measured. No overclaim or artifact.
- **elapsed**: 55.0s

## Hypothesis
Consecutive zeros never collide; the smallest normalized gap stays > 0.

## Claim (entailed by the numbers)
Scanned first 300 zeros: smallest normalized gap 0.2911 between zeros #212 and #213 (heights 415.019, 415.455). All gaps positive; consistent with RH (no collision).

## Metrics
```json
{
  "n_zeros_scanned": 300,
  "min_normalized_gap": 0.29108837445225194,
  "closest_pair": [
    212,
    213
  ],
  "closest_pair_heights": [
    415.01880975515513,
    415.4552149962946
  ],
  "n_gaps": 299
}
```

## Evidence
```json
{
  "method": "unfold via theta/pi; min over consecutive normalized gaps",
  "min_gap": 0.29108837445225194,
  "closest_pair_indices": [
    212,
    213
  ]
}
```

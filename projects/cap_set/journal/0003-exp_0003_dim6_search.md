# Iteration 0003 -- Random-restart greedy cap in F_3^6

- **module**: `projects.cap_set.experiments.exp_0003_dim6_search`
- **track**: `cap_construction`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: cap_size_dim6 = 77.0
- **skeptic**: sound -- Size 77 is a verified valid cap, well below the known max 112 with gap correctly stated; no record or novelty-of-result overclaim. Frontier-search label fits (merely opens cap_size_dim6). Claim uses recomputed baseline 64, beating it honestly. Reproducibility seed recorded. Numbers and interpretation align.
- **elapsed**: 108.1s

## Hypothesis
Randomized greedy builds a large valid cap in F_3^6.

## Claim (entailed by the numbers)
Random-restart greedy (10462 restarts) finds a VALID cap of size 77 in F_3^6 (verified by is_cap), beating the first-fit baseline 64; known maximum 112, gap 35. Best seed 1045.

## Metrics
```json
{
  "dimension": 6,
  "cap_size": 77,
  "valid": true,
  "restarts": 10462,
  "best_seed": 1045,
  "baseline_first_fit": 64,
  "known_max": 112,
  "gap_to_max": 35
}
```

## Evidence
```json
{
  "method": "random-restart greedy; best over seeded priorities; is_cap audited",
  "best_seed": 1045,
  "reproduce": "random.Random(best_seed) priority over cap.vectors(6)"
}
```

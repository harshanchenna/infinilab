# Iteration 0004 -- Evolved priority builds a 76-edge snake in Q_8

- **module**: `projects.snake.experiments.exp_0004_evolved_dim8`
- **track**: `snake_construction`  |  **novelty**: frontier-search
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: snake_len_dim8 = 76.0
- **skeptic**: sound -- audited 76 edges > first-fit 56; optimum 98, gap 22 stated; myopic greedy noted
- **elapsed**: 0.1s

## Hypothesis
The evolved champion priority builds a long valid snake in Q_8.

## Claim (entailed by the numbers)
Evolved priority builds a VALID snake of 76 edges in Q_8 (is_induced_path-verified), beating first-fit baseline 56; proven optimum 98, gap 22.

## Metrics
```json
{
  "dimension": 8,
  "snake_len_edges": 76,
  "valid": true,
  "baseline_first_fit": 56,
  "longest_known": 98,
  "known_is_proven_optimum": true,
  "gap_to_known": 22,
  "is_optimal": false
}
```

## Evidence
```json
{
  "method": "harness.evolve champion priority(v,n); greedy_snake; is_induced_path audited",
  "source": "state/evolve/snake_priority/ (git-tracked program DB)",
  "note": "single deterministic priority (greedy, myopic); not backtracking search"
}
```

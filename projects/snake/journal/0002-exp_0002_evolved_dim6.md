# Iteration 0002 -- Evolved priority builds a 25-edge snake in Q_6

- **module**: `projects.snake.experiments.exp_0002_evolved_dim6`
- **track**: `snake_construction`  |  **novelty**: frontier-search
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: snake_len_dim6 = 25.0
- **skeptic**: sound -- audited 25 edges > first-fit 21; proven optimum 26, gap 1 stated; no overclaim
- **elapsed**: 0.1s

## Hypothesis
The evolved champion priority builds a long valid snake in Q_6.

## Claim (entailed by the numbers)
Evolved priority builds a VALID snake of 25 edges in Q_6 (is_induced_path-verified), beating first-fit baseline 21; proven optimum 26, gap 1.

## Metrics
```json
{
  "dimension": 6,
  "snake_len_edges": 25,
  "valid": true,
  "baseline_first_fit": 21,
  "longest_known": 26,
  "known_is_proven_optimum": true,
  "gap_to_known": 1,
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

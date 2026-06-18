# Iteration 0003 -- Evolved priority builds a 46-edge snake in Q_7

- **module**: `projects.snake.experiments.exp_0003_evolved_dim7`
- **track**: `snake_construction`  |  **novelty**: frontier-search
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: snake_len_dim7 = 46.0
- **skeptic**: sound -- audited 46 edges > first-fit 34; optimum 50, gap 4 stated
- **elapsed**: 0.1s

## Hypothesis
The evolved champion priority builds a long valid snake in Q_7.

## Claim (entailed by the numbers)
Evolved priority builds a VALID snake of 46 edges in Q_7 (is_induced_path-verified), beating first-fit baseline 34; proven optimum 50, gap 4.

## Metrics
```json
{
  "dimension": 7,
  "snake_len_edges": 46,
  "valid": true,
  "baseline_first_fit": 34,
  "longest_known": 50,
  "known_is_proven_optimum": true,
  "gap_to_known": 4,
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

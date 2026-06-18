# Iteration 0001 -- Evolved priority builds a 13-edge snake in Q_5

- **module**: `projects.snake.experiments.exp_0001_evolved_dim5`
- **track**: `snake_construction`  |  **novelty**: frontier-search
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: snake_len_dim5 = 13.0
- **skeptic**: sound -- is_induced_path-audited; 13 edges = proven optimum (n<=8); reaches known max on 2nd domain
- **elapsed**: 0.1s

## Hypothesis
The evolved champion priority builds a long valid snake in Q_5.

## Claim (entailed by the numbers)
Evolved priority builds a VALID snake of 13 edges in Q_5 (is_induced_path-verified) = the PROVEN OPTIMUM 13: the engine reaches the known maximum on a second domain. First-fit baseline 12.

## Metrics
```json
{
  "dimension": 5,
  "snake_len_edges": 13,
  "valid": true,
  "baseline_first_fit": 12,
  "longest_known": 13,
  "known_is_proven_optimum": true,
  "gap_to_known": 0,
  "is_optimal": true
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

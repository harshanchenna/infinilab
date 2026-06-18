# Iteration 0009 -- Evolved structured priority beats best-of-many in F_3^5 (40 > 39)

- **module**: `projects.cap_set.experiments.exp_0009_evolved_dim5`
- **track**: `cap_construction`  |  **novelty**: frontier-search
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: cap_size_dim5 = 40.0
- **skeptic**: sound -- is_cap-audited cap 40 > random-restart frontier 39; gap-to-max 5 stated; no overclaim
- **elapsed**: 0.1s

## Hypothesis
An evolved deterministic priority beats the random-restart frontier (39) in F_3^5.

## Claim (entailed by the numbers)
A single deterministic FunSearch-evolved priority builds a VALID cap of size 40 in F_3^5 (is_cap-verified), beating the prior best-of-many random-restart frontier 39; known maximum 45, gap 5. Evolution now leads every recorded cap frontier (dims 4-7).

## Metrics
```json
{
  "dimension": 5,
  "cap_size": 40,
  "valid": true,
  "prior_frontier_random_restart": 39,
  "known_max": 45,
  "gap_to_max": 5
}
```

## Evidence
```json
{
  "method": "harness.evolve champion priority (weight-layer + hash); is_cap audited",
  "source": "state/evolve/cap_priority/programs/prog_0007.py",
  "note": "single deterministic priority beats best-of-many random restart (39)"
}
```

# Iteration 0008 -- Evolution improves its own F_3^7 cap frontier (148 -> 151)

- **module**: `projects.cap_set.experiments.exp_0008_evolved_dim7`
- **track**: `cap_construction`  |  **novelty**: frontier-search
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: cap_size_dim7 = 151.0
- **skeptic**: sound -- is_cap-audited cap 151 > prior evolved 148; gap-to-max 85 stated; no overclaim
- **elapsed**: 0.2s

## Hypothesis
A further-evolved priority beats the prior evolved dim-7 frontier (148).

## Claim (entailed by the numbers)
A further-evolved deterministic priority builds a VALID cap of size 151 in F_3^7 (is_cap-verified), improving on the prior evolved frontier 148; known maximum 236, gap 85.

## Metrics
```json
{
  "dimension": 7,
  "cap_size": 151,
  "valid": true,
  "prior_frontier": 148,
  "known_max": 236,
  "gap_to_max": 85
}
```

## Evidence
```json
{
  "method": "harness.evolve champion priority (hash base 2.684); is_cap audited",
  "source": "state/evolve/cap_priority/programs/prog_0006.py",
  "note": "single deterministic priority; iterating on its own frontier"
}
```

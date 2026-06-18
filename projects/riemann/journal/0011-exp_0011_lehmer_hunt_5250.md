# Iteration 0011 -- Resolve and measure the close zero pair near T~5250

- **module**: `experiments.exp_0011_lehmer_hunt_5250`
- **track**: `lehmer_pairs`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: inverse_min_normalized_gap = 21.603120501137642
- **skeptic**: sound -- Normalization formula correct (δ≈0.046 reproduces from heights); 267 zeros matches local density so interval fully scanned; raw gap spans ~5.5 grid steps so cleanly resolved, not a sub-step artifact; certified Arb signs make both zeros proven. Claim avoids RH-proof overreach, states record only vs lab's own 0.291, and frontier-search novelty is genuine. Tight but plausible pair; metric backed by real work.
- **elapsed**: 48.8s

## Hypothesis
A near-Lehmer pair sits in (5000,5250]; measure its normalized gap.

## Claim (entailed by the numbers)
Resolved 267 zeros in (5000,5250]; closest pair at heights 5229.1986, 5229.2418 with raw gap 0.04325 and normalized gap delta=0.0463 (NEW lab record close pair (<0.291)). A genuine near-Lehmer pair; all gaps positive, consistent with RH.

## Metrics
```json
{
  "n_zeros_resolved": 267,
  "min_normalized_gap": 0.046289608945491875,
  "raw_gap": 0.0432540597703337,
  "pair_heights": [
    5229.1985571992245,
    5229.241811258995
  ],
  "new_lab_record": true
}
```

## Evidence
```json
{
  "method": "dense certified Arb Z scan + bisection to locate zeros",
  "closest_pair": [
    5229.1985571992245,
    5229.241811258995
  ],
  "normalized_gap": 0.046289608945491875,
  "prior_lab_record": 0.291
}
```

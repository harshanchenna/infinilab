# Iteration 0002 -- GUE vs Poisson nearest-neighbour spacing of zeta zeros

- **module**: `experiments.exp_0002_gue_spacing`
- **track**: `zero_statistics`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: n_zeros_sampled = 200.0
- **skeptic**: sound -- Claim is honestly hedged (consistent with RH, not proof). DPS=20 adequate for height ~396; mean spacing ~1.0 confirms unfolding. KS_gue (0.071) << KS_poisson (0.353) entails the stated prediction. References correct, result correctly framed as known Montgomery-Odlyzko signature, frontier value = actual zeros computed.
- **elapsed**: 21.2s

## Hypothesis
Unfolded zero spacings follow the GUE Wigner surmise.

## Claim (entailed by the numbers)
First 200 zeta zeros: unfolded spacings fit GUE (KS=0.071) far better than Poisson (KS=0.353); mean gap 0.999. Consistent with Montgomery-Odlyzko.

## Metrics
```json
{
  "n_zeros_sampled": 200,
  "ks_gue": 0.0710525599206484,
  "ks_poisson": 0.3525210830169603,
  "mean_spacing": 0.9989933184967451,
  "gue_fits_better": true
}
```

## Evidence
```json
{
  "method": "unfold via theta/pi; KS distance to GUE and Poisson CDFs",
  "n_spacings": 199,
  "gamma_1": 14.134725141734695,
  "gamma_last": 396.3818542225922
}
```

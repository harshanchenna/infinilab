# Iteration 0008 -- Reconstruct Chebyshev psi(x) from zeta zeros (von Mangoldt)

- **module**: `experiments.exp_0008_explicit_formula`
- **track**: `explicit_formula`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: n_zeros_used = 200.0
- **skeptic**: sound -- Residual decreases as N doubles (0.154->0.126), matching the falsifiable prediction. DPS=25 adequate for these zero heights; non-integer grid avoids Gibbs artifacts. Claim is modest ('converging','consistent with RH'), no overclaim of proof. It's a consistency check of the explicit formula rather than an independent RH test, but the wording stays within bounds. frontier_value=200 honest.
- **elapsed**: 28.1s

## Hypothesis
The zero-sum explicit formula reproduces psi(x); residual -> 0 as N grows.

## Claim (entailed by the numbers)
Explicit formula reconstructs psi(x) on 15 points (x in [10.5,80.5]): RMS residual 0.1257 with 200 zeros, down from 0.1540 with 100 zeros. Converging as predicted; consistent with RH.

## Metrics
```json
{
  "n_zeros_used": 200,
  "n_zeros_half": 100,
  "rms_residual_full": 0.1257004086992017,
  "rms_residual_half": 0.15400163096609437,
  "improved_with_more_zeros": true,
  "n_grid_points": 15
}
```

## Evidence
```json
{
  "method": "psi(x) = x - sum 2Re(x^rho/rho) - ln(2pi) - (1/2)ln(1-x^-2) vs exact psi",
  "rms_full": 0.1257004086992017,
  "rms_half": 0.15400163096609437
}
```

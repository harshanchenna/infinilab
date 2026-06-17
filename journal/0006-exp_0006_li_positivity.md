# Iteration 0006 -- Positivity of the first N Keiper-Li coefficients

- **module**: `experiments.exp_0006_li_positivity`
- **track**: `li_criterion`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: n_li_coefficients = 12.0
- **skeptic**: sound -- Well-hedged: claims only 'consistent with Li's criterion,' explicitly not a proof, positivity-signal-only with convergence-from-below correctly framed. Estimates match known true λ_n as lower bounds (λ1≈0.0231, λ2≈0.092, λ3≈0.208). Two-truncation monotonicity guard is sensible. Frontier=12 is just the count checked positive. DPS=30 adequate for 400 zeros. No overclaiming.
- **elapsed**: 73.1s

## Hypothesis
lambda_n >= 0 for all n (Li's criterion <=> RH).

## Claim (entailed by the numbers)
First 12 Keiper-Li coefficients estimated from 400 zeros are all positive (min lambda=0.0231) and increase from K=200 to K=400 (converging from below). Consistent with Li's criterion / RH.

## Metrics
```json
{
  "n_li_coefficients": 12,
  "k_coarse": 200,
  "k_fine": 400,
  "min_lambda_fine": 0.023095708966121033,
  "all_positive": true,
  "monotone_increasing_in_K": true,
  "lambda_fine": [
    0.023095708966121033,
    0.08968667227078865,
    0.19966173421662448,
    0.3528361135743673,
    0.5489521186762236,
    0.7876801439456328,
    1.068619943289256,
    1.3913021745081298,
    1.75519020764433,
    2.159682188973174,
    2.6041133511847634,
    3.087758559178182
  ]
}
```

## Evidence
```json
{
  "method": "power sums: exact S_1 + truncated S_j; lambda_n via binomial sum",
  "lambda_coarse": [
    0.023095708966121033,
    0.08822404171477692,
    0.1952738513668582,
    0.34406037139017576,
    0.5343259306927466,
    0.7657409501524696,
    1.0379052160089974,
    1.3503494242747498,
    1.7025369890814093,
    2.0938661066719306,
    2.5236720655818634,
    2.9912297924333084
  ],
  "lambda_fine": [
    0.023095708966121033,
    0.08968667227078865,
    0.19966173421662448,
    0.3528361135743673,
    0.5489521186762236,
    0.7876801439456328,
    1.068619943289256,
    1.3913021745081298,
    1.75519020764433,
    2.159682188973174,
    2.6041133511847634,
    3.087758559178182
  ],
  "note": "estimates approach true positive values from below; positivity signal only"
}
```

# Iteration 0013 -- Robin violation hunt over colossally abundant numbers

- **module**: `experiments.exp_0012_robin_colossally_abundant`
- **track**: `robin_inequality`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: max_robin_ratio_CA = 0.9978871557561669
- **skeptic**: sound -- Honest, conservative falsification-attempt over the true extremal family (CA numbers). No proof or falsification claimed; correctly reports max f=0.9979<1 as closest approach within the searched range. Exact f(n) from factorization; 50 dps ample for O(1) ratios at ln n~2789. frontier_value genuinely backed. The 0.9979 just reflects where the walk stopped (f→1 by Gronwall), which the claim states honestly.
- **elapsed**: 0.4s

## Hypothesis
No CA number n>5040 violates Robin (f(n) stays < 1).

## Claim (entailed by the numbers)
Hunted 1456 colossally abundant numbers n>5040 (up to ln n=2788.8, ~1211 digits): max Robin ratio f=0.997887 < 1. No violation -> consistent with RH on the true extremal family (closest approach 0.997887).

## Metrics
```json
{
  "n_CA_total": 1464,
  "n_CA_above_5040": 1456,
  "max_robin_ratio_CA": 0.9978871557561669,
  "max_ratio_ln_n": 2788.8053776207284,
  "violation": false
}
```

## Evidence
```json
{
  "method": "Alaoglu-Erdos CA generation; exact f(n) from factorization",
  "max_robin_ratio": 0.9978871557561669,
  "violation": null,
  "largest_ln_n": 2788.8053776207284
}
```

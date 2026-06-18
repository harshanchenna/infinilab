# Iteration 0015 -- de Bruijn-Newman lower bound from the gamma~5229 Lehmer pair

- **module**: `experiments.exp_0014_de_bruijn_newman`
- **track**: `de_bruijn_newman`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: lambda_lower_bound = -0.00023411610422963117
- **skeptic**: sound -- Numbers internally consistent (lambda≈-delta^2/8, factor<<1, valid pair). Claim is conservative and explicitly acknowledges it is far weaker than the world record and consistent with Rodgers-Tao Lambda>=0. No overclaim of proof. Caveat: bound is trivially weaker than proven Lambda>=0, so frontier_value advances nothing — but framing is honest about this, not deceptive. Genuine computed bound from a self-discovered pair.
- **elapsed**: 139.6s

## Hypothesis
Our close pair yields a valid lower bound Lambda >= lambda_k < 0.

## Claim (entailed by the numbers)
From the Lehmer pair at heights 5229.1986, 5229.2418 (index 4765, gap 0.04325): valid Lehmer pair ((5/4)delta^2 g_k=0.0107<1, g_k=4.5858), giving Lambda >= -2.341e-04. A genuine (modest) lower bound on the de Bruijn-Newman constant from a pair we discovered; consistent with RH (Lambda<=0 unproven) and with Lambda>=0 (Rodgers-Tao).

## Metrics
```json
{
  "pair_index": 4765,
  "gamma_k": 5229.19855719922,
  "gamma_k1": 5229.241811258999,
  "raw_gap": 0.04325405977869733,
  "g_k": 4.585841206887864,
  "validity_factor": 0.010724641352412828,
  "valid_lehmer_pair": true,
  "lambda_lower_bound": -0.00023411610422963117,
  "window_zeros_each_side": 100,
  "gk_tail_scale": 0.0004530699993643925
}
```

## Evidence
```json
{
  "method": "Csordas-Smith-Varga (1994) Lehmer-pair bound on Lambda",
  "lambda_lower_bound": -0.00023411610422963117,
  "leading_term_-delta2_over_8": -0.0002338642109173903,
  "world_record_for_context": -1.14e-11
}
```

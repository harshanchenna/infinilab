# Iteration 0007 -- Certified (Arb) verification of zeros on the critical line

- **module**: `experiments.exp_0007_certified_verification`
- **track**: `certified_zero_verification`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: certified_T = 150.0
- **skeptic**: sound -- Certified ≥52 on-line zeros is a correct sign-change lower bound; 256 bits and step 0.125 (~10 samples/gap) are adequate at T=150, no resolution risk. The 'RH verified up to T' depends on uncertified mpmath N(T)=52, but this is explicitly labeled Turing and not overstated as certified. No 'proves RH', frontier=150 backed by real computation.
- **elapsed**: 0.4s

## Hypothesis
Every zero up to height T is provably on Re=1/2.

## Claim (entailed by the numbers)
CERTIFIED: at least 52 zeros proven on the critical line up to T=150.00 via Arb ball arithmetic; matches N(T)=52 (Turing) with no uncertified points -> RH verified up to T=150.00.

## Metrics
```json
{
  "T": 150.0,
  "prec_bits": 256,
  "step": 0.125,
  "certified_sign_changes": 52,
  "n_exact_NT": 52,
  "n_uncertified_points": 0,
  "matched_NT": true,
  "clean_certified_T": 150.0
}
```

## Evidence
```json
{
  "method": "Arb rigorous Hardy-Z enclosures; certified sign changes = proven on-line zeros",
  "proven_on_line_zeros": 52,
  "matched_NT": true
}
```

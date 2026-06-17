# Knowledge base

Skeptic-vetted, reproducible facts kept by the loop.

- **[zero_verification]** All 52 nontrivial zeros with 0 < Im < 150.00 lie on the critical line: Hardy Z has exactly N(T)=52 sign changes. (iter 1, `exp_0001_critical_line`, T_verified=150, skeptic=sound)

- **[zero_statistics]** First 200 zeta zeros: unfolded spacings fit GUE (KS=0.071) far better than Poisson (KS=0.353); mean gap 0.999. Consistent with Montgomery-Odlyzko. (iter 2, `exp_0002_gue_spacing`, n_zeros_sampled=200, skeptic=sound)

- **[lehmer_pairs]** Scanned first 300 zeros: smallest normalized gap 0.2911 between zeros #212 and #213 (heights 415.019, 415.455). All gaps positive; consistent with RH (no collision). (iter 3, `exp_0003_lehmer_pairs`, n_zeros_scanned=300, skeptic=sound)

- **[zero_verification]** All 341 nontrivial zeros with 0 < Im < 600.00 lie on the critical line: Hardy Z has exactly N(T)=341 sign changes. (iter 4, `exp_0004_critical_line_high`, T_verified=600, skeptic=sound)

- **[robin_inequality]** Robin's inequality holds for all 1995 primorials P_k > 5040 up to k=2000: max ratio f=0.77546 at k=6 (< 1). Consistent with RH on the primorial family. (iter 5, `exp_0005_robin_primorials`, n_primorials_checked=1995, skeptic=sound)

- **[li_criterion]** First 12 Keiper-Li coefficients estimated from 400 zeros are all positive (min lambda=0.0231) and increase from K=200 to K=400 (converging from below). Consistent with Li's criterion / RH. (iter 6, `exp_0006_li_positivity`, n_li_coefficients=12, skeptic=sound)

- **[certified_zero_verification]** CERTIFIED: at least 52 zeros proven on the critical line up to T=150.00 via Arb ball arithmetic; matches N(T)=52 (Turing) with no uncertified points -> RH verified up to T=150.00. (iter 7, `exp_0007_certified_verification`, certified_T=150, skeptic=sound)


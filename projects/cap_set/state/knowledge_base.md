# Knowledge base

Skeptic-vetted, reproducible facts kept by the loop.

- **[cap_construction]** First-fit greedy builds a VALID cap of size 32 in F_3^5 (verified by is_cap; known maximum 45, gap 13). Baseline. (iter 1, `exp_0001_greedy_baseline`, cap_size_dim5=32, skeptic=sound)

- **[cap_construction]** Random-restart greedy (26954 restarts) finds a VALID cap of size 39 in F_3^5 (verified by is_cap), beating the first-fit baseline 32; known maximum 45, gap 6. Best seed 874. (iter 2, `exp_0002_random_restart`, cap_size_dim5=39, skeptic=sound)

- **[cap_construction]** Random-restart greedy (10462 restarts) finds a VALID cap of size 77 in F_3^6 (verified by is_cap), beating the first-fit baseline 64; known maximum 112, gap 35. Best seed 1045. (iter 3, `exp_0003_dim6_search`, cap_size_dim6=77, skeptic=sound)


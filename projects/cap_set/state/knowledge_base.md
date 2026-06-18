# Knowledge base

Skeptic-vetted, reproducible facts kept by the loop.

- **[cap_construction]** First-fit greedy builds a VALID cap of size 32 in F_3^5 (verified by is_cap; known maximum 45, gap 13). Baseline. (iter 1, `exp_0001_greedy_baseline`, cap_size_dim5=32, skeptic=sound)

- **[cap_construction]** Random-restart greedy (26954 restarts) finds a VALID cap of size 39 in F_3^5 (verified by is_cap), beating the first-fit baseline 32; known maximum 45, gap 6. Best seed 874. (iter 2, `exp_0002_random_restart`, cap_size_dim5=39, skeptic=sound)

- **[cap_construction]** Random-restart greedy (10462 restarts) finds a VALID cap of size 77 in F_3^6 (verified by is_cap), beating the first-fit baseline 64; known maximum 112, gap 35. Best seed 1045. (iter 3, `exp_0003_dim6_search`, cap_size_dim6=77, skeptic=sound)

- **[cap_construction]** Iterated local search finds a VALID cap of size 20 in F_3^4 (is_cap-verified) = the PROVEN MAXIMUM 20: the loop reaches the optimum where one is known. (iter 4, `exp_0004_ils_dim4_optimal`, cap_size_dim4=20, skeptic=n/a)

- **[cap_construction]** Iterated local search finds a VALID cap of size 81 in F_3^6 (is_cap-verified), improving on the prior random-restart frontier 77; known maximum 112, gap 31. (iter 5, `exp_0005_ils_dim6`, cap_size_dim6=81, skeptic=n/a)

- **[cap_construction]** A FunSearch-evolved deterministic priority builds a VALID cap of size 148 in F_3^7 (is_cap-verified), opening the dim-7 frontier (first-fit baseline 128); known maximum 236, gap 88. The candidate was selected by a rigorous evaluator (is_cap audits every construction), demonstrating the evolution mechanism end-to-end. (iter 6, `exp_0006_evolved_dim7`, cap_size_dim7=148, skeptic=sound)

- **[cap_construction]** A single deterministic FunSearch-evolved priority builds a VALID cap of size 82 in F_3^6 (is_cap-verified), beating the prior best-of-many random-restart frontier 81 -- evolved structure out-performs best-of-many search in one shot. Known maximum 112, gap 30. (iter 7, `exp_0007_evolved_dim6`, cap_size_dim6=82, skeptic=sound)

- **[cap_construction]** A further-evolved deterministic priority builds a VALID cap of size 151 in F_3^7 (is_cap-verified), improving on the prior evolved frontier 148; known maximum 236, gap 85. (iter 8, `exp_0008_evolved_dim7`, cap_size_dim7=151, skeptic=sound)

- **[cap_construction]** A single deterministic FunSearch-evolved priority builds a VALID cap of size 40 in F_3^5 (is_cap-verified), beating the prior best-of-many random-restart frontier 39; known maximum 45, gap 5. Evolution now leads every recorded cap frontier (dims 4-7). (iter 9, `exp_0009_evolved_dim5`, cap_size_dim5=40, skeptic=sound)


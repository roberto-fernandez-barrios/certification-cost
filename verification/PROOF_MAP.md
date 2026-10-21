# Certificate-to-result map

[Repository home](../README.md) · [Reproduction guide](../docs/REPRODUCIBILITY.md) · [Scope and alignment](../docs/SCOPE.md)

References below are to the accompanying article, whose essential proofs are in Appendices A–E. The manuscript is supplied separately for editorial review.

| Obligation | Existing input / check | Required analytic argument |
|---|---|---|
| Universal unilateral lower bound | dual_lower.json / bellman | B-C: free abandonment relaxes every integrable policy; valid lower rounding. |
| Localize all dual maximizers | mixture_certificate.json, dual_localization.json / profiles, tail | B-C: strict feasibility, coercivity, semicontinuity, exclusion of axes. |
| Attain the dual without restricting competitors | bellman_localization.json / bellman | B-D: concavity, contact, multiplier monotonicity and stopped verification. |
| Entire box and continuous domain D | box_certificate_full.json / box, tail | B-A–B-B: exact partition, all ties, Bernstein signs on intervals, survival after 400. |
| Infinite horizon | Rational endpoint bounds / tail, profiles | B-A: integrability before drift, remainder below 600, uniform geometric tail. |
| Exactly feasible optimal mixture | Not certified by an approximate rational mixture | B-E: compact profiles, separation, at most three active slopes, errors exactly alpha. |
| Scalar equality and obligation for every test | Above inputs | B-C–B-E: other endpoint below 212, dual above 262, unilateral bound and attaining mixture. |
| Implemented rational mixture | scalar_1e6.json / profiles | B-E and VI-A: infinite-tail risk bounds; U minus ell permits cost tolerance only. |
| Global observable reduction | Functions f, g and selector / factory | A: smooth interior factory theorem, global algebra, freshness, summable tail. |
| Executable factory at all levels | factory.json, composition.json / independent_factory.py | E: derivatives, moments, elevation, sum of tails; no finite CPU theorem. |
| Oracle and upper bound | Model, scalar optimum, transformation | C: fresh coin per measurement, predictable attainability, Tonelli, distinct labels. |
| Cache variant | Same scalar mixture and selector | Supplement S1/H1: marked-law equality and freshness after internal stopping. |
| Excess lower bound | Same nominal world and policy | D: universal measurement obligation, label coupling/incidence, add before optimizing and subtract the exact oracle. |
| Hypergeometric refinement | No new dependency on the certificates in this repository | Proposition 1 and D-E: exact subset counting, decreasing increments, concave interpolation, Jensen, and the same nominal world. The separate arithmetic check is outside this public package. |

The ten mathematical inputs retain their original bytes. Hashes identify these inputs; they do not establish mathematical correctness. This package runs no new experiments.

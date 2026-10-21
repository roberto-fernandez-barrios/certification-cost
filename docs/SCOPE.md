# Scope and alignment with the manuscript

[Repository home](../README.md) · [Reproduction guide](REPRODUCIBILITY.md) · [Proof map](../verification/PROOF_MAP.md)

## What this repository verifies

The public companion contains eight existing JSON certificates, two independent checking scripts, their original input manifest, and the reproduction runner. Its five deterministic checks recompute finite or symbolic ingredients of the scalar closure and Bernoulli-factory construction.

The [certificate-to-result map](../verification/PROOF_MAP.md) connects those ingredients to the manuscript's arguments. Success of the scripts does not, by itself, establish compactness, unbounded-horizon validity, continuous-domain coverage, unrestricted-policy coverage, or the same-world coupling. Those require the written analytical proofs.

## Mathematical distinctions retained

- The exact label-oracle value is an analytical equality; it is not obtained by rounding a numerical interval to a point.
- The exact existential optimum and the implemented rational mixture are different objects. The latter retains a positive tolerance in **cost only**, with unchanged risk.
- Measurement and label obligations must hold in the same nominal world. They are added before optimizing, followed by subtraction of the exact oracle value.
- Distinct purchased labels differ from repeated visits and cache hits.
- Complementary results C1 and C2 have their own assumptions and do not enlarge the principal contract.
- The work does not establish joint optimality of the implemented policy, practical computational efficiency, or quantum advantage.

## Relationship to the final companion manuscript

The manuscript retains its original Theorem 1 and adds a hypergeometric refinement in Proposition 1 and Appendix D-E. That refinement is analytical: exact subset counting, discrete concavity, and Jensen's inequality strengthen the label lower bound under the original assumptions. It does not change any of this repository's eight certificates or two checkers.

The refinement's separate arithmetic check is supplied with the manuscript's research records. It is not one of the five checks in this repository. A green workflow badge must not be interpreted as execution of that additional check or verification of the complete proposition.

The following materials are supplied separately:

| Material | Role |
|---|---|
| `manuscript.pdf` | Main article and essential analytical proofs, including Appendices A–E |
| `supplementary_material.pdf` | Accounting, historical comparisons, complementary contracts, and reproduction instructions |
| `verification_package.zip` | The same original scientific verification inputs provided for editorial review |
| `historical_reproduction.zip` | Archived records and deterministic reconstruction of the historical tables |

The historical archive verifies 59 input identities and reconstructs 48 original cells with eight replacement continuations and 16 later replays. This public repository does **not** contain or rerun that historical archive. Reconstruction of archived records is different from generating new experiments, and continuations are not additional independent replicates.

The manuscript and editorial materials are not published here. See [provenance](PROVENANCE.md) for the exact manuscript fingerprint and the original public input snapshot.

## Interpretation of evidence

Hashes identify bytes relative to a manifest. They do not prove authenticity or mathematical truth. Finite checks verify their declared ingredients, not a general theorem by enumeration. The CI badge reports automated execution, not peer review, editorial acceptance, or formal proof verification.

The companion manuscript is unpublished; this repository makes no claim of journal acceptance. The public verification companion is licensed under [MIT](../LICENSE) and has a separate [software DOI](https://doi.org/10.5281/zenodo.23529082). This licence and DOI apply to the public companion, not to the separately supplied manuscript or private archives.

# Certification Cost

**Verification companion for _The Price of Missing Labels in Certification with Unknown Readout_.**

[![Deterministic verification](https://github.com/roberto-fernandez-barrios/certification-cost/actions/workflows/verify.yml/badge.svg?branch=main)](https://github.com/roberto-fernandez-barrios/certification-cost/actions/workflows/verify.yml)
[![Software DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23529082.svg)](https://doi.org/10.5281/zenodo.23529082)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[Reproduction guide](docs/REPRODUCIBILITY.md) · [Proof map](verification/PROOF_MAP.md) · [Scope](docs/SCOPE.md) · [Citation](CITATION.cff)

How much does acquiring missing labels add to certification cost when knowing every label still leaves the measurement channel unknown? The companion manuscript studies this question through a comparison of joint acquisition and label-oracle costs under the same error requirement in every permitted world.

This repository provides the **five deterministic checks, eight exact certificates, and provenance records** supporting the manuscript's scalar and factory calculations. It requires Python 3.13 and its standard library. The analytical arguments are supplied in the manuscript; the executable checks verify their stated finite or symbolic ingredients.

**Authors:** [Roberto Fernández-Barrios](https://orcid.org/0009-0003-5312-2634), [Iker Pastor-López](https://orcid.org/0000-0002-3068-6248), [Rubén López De Juan](https://orcid.org/0009-0002-0445-9030), and [Pablo García Bringas](https://orcid.org/0000-0003-3594-9534). University of Deusto, Spain.

## Quick start

Clone the repository, or download and extract its ZIP from GitHub's **Code** menu. From the repository root, run:

```sh
python -B -X utf8 tools/verify_repository.py
python -B -X utf8 verification/reproduce.py --output verification_output
```

Use a **new output directory** for each run. On systems where Python 3.13 is named `python3`, use that executable instead. No package installation, solver, credentials, network access, or random experiment is required to run the checks.

A successful reproduction reports **five zero exit codes** and writes `verification_output/EXECUTION_RECORD.json` with `status: COMPLETED` and `input_files_unchanged: 10`, alongside five logs and five check reports. See the [guide](docs/REPRODUCIBILITY.md) for the individual checks, expected files, timing, and troubleshooting.

## Find the evidence

| Resource | Purpose |
|---|---|
| [Reproduction guide](docs/REPRODUCIBILITY.md) | Commands, environment, outputs, and continuous integration |
| [Certificate-to-result map](verification/PROOF_MAP.md) | Each computational ingredient and its remaining analytical obligation |
| [Input manifest](verification/INPUT_MANIFEST.json) | SHA-256 identities and provenance of the eight certificates and two checkers |
| [Repository checksums](SHA256SUMS.txt) | Identities of the distributed files, checked by `tools/verify_repository.py` |
| [Scope and manuscript alignment](docs/SCOPE.md) | Coverage, limitations, and the separately supplied historical material |
| [Provenance](docs/PROVENANCE.md) | Original public snapshot and preservation of scientific inputs |
| [Reporting a problem](CONTRIBUTING.md) | How to report a reproducibility issue with useful evidence |

The workflow badge reports execution of the checks on Linux and Windows. It does not certify the full theorem, formal correctness, or the complete software runtime. The distinction between an exact existential optimum and the implemented rational mixture is preserved; the implementation tolerance concerns cost only. The work does not establish practical efficiency or quantum advantage.

## Citation

The companion manuscript is currently unpublished. Cite it without inventing a journal volume, DOI, or acceptance status:

> R. Fernández-Barrios, I. Pastor-López, R. López De Juan, and P. García Bringas, “The Price of Missing Labels in Certification with Unknown Readout,” unpublished manuscript, 2026.

The software archive has its own citation: Fernández-Barrios, R., Pastor-López, I., López De Juan, R., and García Bringas, P. (2026). _Certification Cost: deterministic verification companion_ (Version 1.0.0). Zenodo. https://doi.org/10.5281/zenodo.23529082.

[CITATION.cff](CITATION.cff) distinguishes the software DOI from the unpublished companion manuscript. When reporting a computational reproduction, also record the repository commit and retain `EXECUTION_RECORD.json` and its logs.

## Availability and contact

The manuscript, supplement, historical reproduction archive, and editorial material are supplied separately. This public repository contains the verification companion; [scope and alignment](docs/SCOPE.md) explains the boundary.

The public code, certificates, and accompanying documentation are distributed under the [MIT License](LICENSE). Version 1.0.0 is identified by the [Zenodo software DOI](https://doi.org/10.5281/zenodo.23529082); this DOI identifies the verification companion, not the article. See [provenance](docs/PROVENANCE.md) for the archival boundary.

Corresponding author: **Roberto Fernández-Barrios** — [roberto.fernandez.b@deusto.es](mailto:roberto.fernandez.b@deusto.es).

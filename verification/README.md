# Certification cost: deterministic verification package

[Repository home](../README.md) · [Reproduction guide](../docs/REPRODUCIBILITY.md) · [Scope and alignment](../docs/SCOPE.md)

Companion code and certificates for *The Price of Missing Labels in Certification with Unknown Readout*.

The eight JSON certificates and two checking scripts are unchanged mathematical inputs. `INPUT_MANIFEST.json` identifies their SHA-256 digests and provenance. No historical datasets, manuscript, credentials, software environment, or experiment runner is included.

## Run

Requirement: Python 3.13 (standard library only). Checked with Python 3.13.12 on Windows x86-64. No network, solver, package installation, or random experiment is needed. From this directory:

```text
python -B -X utf8 reproduce.py --output ../verification_output
```

Choose a new output directory outside this package. The runner verifies the ten input hashes, copies the inputs there, and runs these existing checks with a 180-second limit per process:

```text
python -B -X utf8 independent_checks.py bellman
python -B -X utf8 independent_checks.py box
python -B -X utf8 independent_checks.py profiles
python -B -X utf8 independent_checks.py tail
python -B -X utf8 independent_factory.py
```

Expected result: five exit codes of zero, an `EXECUTION_RECORD.json` with status `COMPLETED` and `input_files_unchanged: 10`, five logs, and the individual JSON check reports. The recorded clean run took approximately 48 seconds in total; this is an observed execution time, not a runtime guarantee. Directory names under `isolated_artifact/` are retained because they are part of the existing checker interface.

## Meaning and limits

`PROOF_MAP.md` maps the inputs to the accompanying article's arguments. The scripts check finite or symbolic ingredients. The analytic arguments for infinite horizons, continuous domains, unrestricted policies, compactness, exact convex closure, emulation and coupling are additional obligations. A successful run is not a formal verification of the whole theorem or runtime. It does not prove finite expected CPU consumption. The exact optimal existential mixture and implemented rational mixture are different objects; the latter's delta is a cost tolerance only, with unchanged risk. Complementary results C1 and C2 have separate contracts.

## Availability and rights

The author authorized this code-and-certificate repository to be public on 19 October 2026 and authorized its MIT-licensed Zenodo deposit on 21 October 2026. The same scientific inputs accompany editorial review. The public companion is distributed under the [MIT License](../LICENSE), with [software DOI 10.5281/zenodo.23529082](https://doi.org/10.5281/zenodo.23529082). The article, supplement, cover letter and private administrative archive are not distributed in this repository.

Contact: Roberto Fernández-Barrios, roberto.fernandez.b@deusto.es.

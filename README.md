# certification-cost

Deterministic verification code and essential certificates accompanying **The Price of Missing Labels in Certification with Unknown Readout**.

This is the minimal reproducibility edition of the project. It contains the existing checking scripts and eight certificate files, with exact input hashes and a proof-dependency map. It does not contain the manuscript, supplement, editorial correspondence, private administrative records, or the complete historical development tree.

## Reproduce the checks

Python 3.13, standard library only:

```text
cd verification
python -B -X utf8 reproduce.py --output ../verification_output
```

See [verification/README.md](verification/README.md) for expected outputs, environment, scope and limitations, and [PROOF_MAP.md](verification/PROOF_MAP.md) for the correspondence with the scientific arguments. These checks do not constitute formal verification of the complete theorem or software runtime. No experiments or simulations are launched.

## Rights and contact

Public distribution of this code and certificate package was authorized by the corresponding author. No software licence or DOI has been assigned. Public availability should not be described as an open-source licence.

Roberto Fernández-Barrios — roberto.fernandez.b@deusto.es.

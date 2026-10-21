# Reporting reproducibility issues

This repository accompanies a fixed scientific result. Useful contributions include reproducible execution reports, documentation corrections, and concrete discrepancies between a certificate, checker, and the associated proof obligation.

Use the [reproducibility issue form](https://github.com/roberto-fernandez-barrios/certification-cost/issues/new?template=reproducibility.yml), or contact [Roberto Fernández-Barrios](mailto:roberto.fernandez.b@deusto.es).

Please include:

1. The repository commit, operating system, and full Python version.
2. The exact command and whether it was run from a fresh download.
3. The expected and observed outcome, including the failing check.
4. `EXECUTION_RECORD.json` and the relevant log, when they exist.

Share only the material needed to reproduce the issue. Keep credentials, unpublished manuscripts, correspondence, and private administrative records out of public issues.

## Preservation when proposing changes

Keep mathematical input changes separate from documentation or automation changes. Do not regenerate a certificate or its input manifest merely to make a check pass. A mathematical correction needs an explicit derivation and a record of which guarantee changes.

Before proposing a repository change, run:

```sh
python -B -X utf8 tools/verify_repository.py
python -B -X utf8 verification/reproduce.py --output verification_output
git diff --check
```

Documentation changes require a corresponding update of the distribution checksum manifest. The scientific input manifest stays unchanged unless a separately justified scientific revision is accepted. Existing input files retain their original line endings.

The public code and accompanying materials are distributed under the [MIT License](LICENSE). Proposed contributions must be compatible with that licence. This document is not a separate contribution licence agreement.

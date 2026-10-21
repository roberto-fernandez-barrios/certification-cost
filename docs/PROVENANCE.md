# Provenance and stable inputs

[Repository home](../README.md) · [Scope](SCOPE.md)

## Original public snapshot

The original public verification companion was published on 19 October 2026 at commit
[`4f5d5dfc83ce5dcf39db600cc37aaff5fe5486f7`](https://github.com/roberto-fernandez-barrios/certification-cost/tree/4f5d5dfc83ce5dcf39db600cc37aaff5fe5486f7).

The eight JSON certificates and two mathematical checkers are identified by [verification/INPUT_MANIFEST.json](../verification/INPUT_MANIFEST.json). The manifest records their existing provenance. Their bytes, the input manifest, and the original `verification/reproduce.py` runner remain unchanged in the documentation and automation update of 21 October 2026.

The repository retains historical directory names under `verification/isolated_artifact/` because the original checkers use those paths. Renaming them for appearance would change the established checker interface.

## Companion manuscript fingerprint

The public code supports the separately supplied version of **The Price of Missing Labels in Certification with Unknown Readout** identified by:

| Supplied file | SHA-256 |
|---|---|
| `manuscript.pdf` | `1bdcea7c4e4efae11967a0e8c3a274348ccd5e24e29d3b253ea0d0b342cf0025` |
| `supplementary_material.pdf` | `f5b88a59cd81c72b150188bd8ca62be6246ca6f02152814aa87113c813ba29fc` |

These fingerprints let a recipient identify the accompanying files; they are not download links or claims of publication. The [scope document](SCOPE.md) explains the additional analytical refinement and separately supplied historical archive.

## Archival software release

Version 1.0.0 (21 October 2026) has software DOI [10.5281/zenodo.23529082](https://doi.org/10.5281/zenodo.23529082) and is distributed under the [MIT License](../LICENSE). The Zenodo record identifies the exact Git commit. Its ZIP contains only the tracked public repository files, including this documentation, the original certificates, and the checkers. It excludes Git internals, the manuscript, the supplement, historical reproduction materials, and private editorial records.

This licensing and archiving update changes no mathematical input or checker. The separately supplied manuscript fingerprints above remain unchanged. Any earlier availability statement describing the absence of a software licence or DOI records the position before this release.

## Distribution integrity

[SHA256SUMS.txt](../SHA256SUMS.txt) covers every distributed repository file except itself. Its contents describe the current distribution. Previous versions remain available in Git history. The separate scientific input manifest remains unchanged.

Run from the repository root:

```sh
python -B -X utf8 tools/verify_repository.py
```

The check rejects missing files, unsafe paths, and byte mismatches, and separately checks the ten original mathematical inputs. It does not rewrite a file or manifest. Downloaded ZIPs can be checked without Git or additional Python packages.

Record the commit, Python version, platform, receipt, and logs when reporting a reproduction. A file hash and a passing execution are different kinds of evidence; neither replaces the written proof.

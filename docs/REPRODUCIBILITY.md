# Reproducing the deterministic checks

[Repository home](../README.md) · [Proof map](../verification/PROOF_MAP.md) · [Scope](SCOPE.md)

## Environment

- Python **3.13**, standard library only.
- The recorded local reference run used Python 3.13.12 on Windows x86-64.
- GitHub Actions runs the same five checks on Ubuntu and Windows with Python 3.13. The [workflow history](https://github.com/roberto-fernandez-barrios/certification-cost/actions/workflows/verify.yml) identifies the actual commit, platform, Python version, and outcome of each run.
- No third-party Python packages, solver, QPU, credentials, or network connection are needed after downloading the repository. No seed is required: these checks use no random sampling.

The workflow outcome is execution evidence for the specified checks. It is not a guarantee for all Python versions or platforms.

## Run from the repository root

Check which Python executable you are using:

```sh
python --version
```

Then verify the distribution and run the scientific checkers:

```sh
python -B -X utf8 tools/verify_repository.py
python -B -X utf8 verification/reproduce.py --output verification_output
```

The first command checks the repository checksums and the ten immutable scientific inputs. The second verifies those inputs again, copies them to the new output directory, and runs each checker in that isolated copy. The source package is not modified. Use a different output directory, such as `verification_output_2`, when repeating a run.

Git is optional for executing the downloaded files. For an auditable reproduction from a clone, also record:

```sh
git rev-parse HEAD
```

## Expected outputs

The runner prints five lines ending in `exit 0`. Its final receipt contains:

```json
{
  "status": "COMPLETED",
  "input_files_unchanged": 10
}
```

This is an excerpt. The actual `EXECUTION_RECORD.json` also contains the Python version, commands, durations, exit codes, log paths, and scope of verification.

| Check | Output report | Ingredient checked |
|---|---|---|
| `independent_checks.py bellman` | `independent_bellman.json` | Directed Bellman calculations and localization margins |
| `independent_checks.py box` | `independent_box.json` | Exact threshold-box and tie checks |
| `independent_checks.py profiles` | `independent_profiles.json` | Stored profiles and rational implementation calculations |
| `independent_checks.py tail` | `independent_tail.json` | Stored tail and sign calculations |
| `independent_factory.py` | `independent_factory.json` | Factory algebra, derivative and moment calculations |

Five text logs, `01.log` through `05.log`, retain standard output and standard error. The [proof map](../verification/PROOF_MAP.md) states what each computation supports and which analytical arguments remain separate.

The original recorded local run took approximately **48 seconds** in total. This is an observation on the recorded machine, not a runtime guarantee. Each checker has a 180-second process timeout. A timeout or nonzero exit code is a failed or incomplete run, never a successful verification.

## Inspect or rerun one check

After the runner has created the isolated output directory, enter that directory and execute the desired command:

```sh
cd verification_output
python -B -X utf8 independent_checks.py bellman
python -B -X utf8 independent_checks.py box
python -B -X utf8 independent_checks.py profiles
python -B -X utf8 independent_checks.py tail
python -B -X utf8 independent_factory.py
```

Do this in a separate working copy if you need to preserve an earlier run's reports. Individual commands do not replace the aggregate receipt from a fresh complete run.

## Continuous integration

The [workflow](../.github/workflows/verify.yml) runs the integrity check and the original reproduction runner on pushes to `main`, pull requests, and manual dispatch. It uses read-only repository permissions and pins the checkout, Python setup, and artifact actions to exact commits.

Each platform stores its receipt, five logs, and five reports as a short-lived workflow artifact. The badge shows execution status for `main`; it is not a mathematical certification badge. CI does not execute historical simulations, alter certificates, publish a manuscript, or regenerate scientific inputs.

## Troubleshooting

| Symptom | Action |
|---|---|
| `python` is missing or identifies another version | Use your Python 3.13 executable, for example `python3` or `py -3.13`. |
| Output directory already exists | Select a new directory; the runner intentionally refuses to overwrite earlier evidence. |
| Output directory is inside `verification/` | Choose a sibling directory such as `verification_output` at the repository root. |
| Hash mismatch | Compare against a fresh download of the same commit. Do not rewrite a certificate or its manifest to silence the mismatch. |
| Checker exits nonzero | Retain the receipt and the named log; report the command, commit, Python version, and platform. |
| A checker exceeds 180 seconds | Record the timeout as incomplete. Do not report a successful verification. |

For a reproducibility report, follow [CONTRIBUTING.md](../CONTRIBUTING.md).

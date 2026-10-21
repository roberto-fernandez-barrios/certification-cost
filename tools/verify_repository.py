"""Check published file identities and immutable inputs using the standard library."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def checked_path(root: Path, relative: str) -> Path:
    """Accept a regular file below root, without traversal or symlink components."""
    name = PurePosixPath(relative)
    if (not relative or "\\" in relative or ":" in relative
            or name.is_absolute() or ".." in name.parts
            or name.as_posix() != relative):
        raise ValueError(f"Unsafe manifest path: {relative!r}")
    candidate = root
    for part in name.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError(f"Symlink in manifest path: {relative}")
    if not candidate.is_file():
        raise ValueError(f"Missing regular file: {relative}")
    if root.resolve() not in candidate.resolve().parents:
        raise ValueError(f"Path leaves package: {relative}")
    return candidate


def verify_hash(path: Path, expected: str) -> None:
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError(f"Invalid SHA-256 entry for {path.name}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f"SHA-256 mismatch: {path.relative_to(ROOT)}")


def main() -> int:
    try:
        seen: set[str] = set()
        lines = (ROOT / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
        for number, line in enumerate(lines, 1):
            if not line.strip():
                continue
            if "  " not in line:
                raise ValueError(f"Malformed checksum entry on line {number}")
            expected, relative = line.split("  ", 1)
            if relative in seen or relative == "SHA256SUMS.txt":
                raise ValueError(f"Duplicate or self-referential entry: {relative}")
            seen.add(relative)
            verify_hash(checked_path(ROOT, relative), expected)
        if not seen:
            raise ValueError("Empty checksum manifest")

        package = ROOT / "verification"
        inputs = json.loads((package / "INPUT_MANIFEST.json").read_text(encoding="utf-8"))
        if not isinstance(inputs, dict) or len(inputs) != 10:
            raise ValueError("Expected ten original scientific inputs")
        for relative, record in inputs.items():
            if "verification/" + relative not in seen:
                raise ValueError(f"Scientific input absent from distribution manifest: {relative}")
            verify_hash(checked_path(package, relative), record["sha256"])
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Integrity check failed: {error}", file=sys.stderr)
        return 1

    print(f"Verified {len(seen)} distribution files and {len(inputs)} original scientific inputs.")
    print("Byte identity only; not authenticity, mathematical proof, or peer review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

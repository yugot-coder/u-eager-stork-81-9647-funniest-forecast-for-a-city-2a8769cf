#!/usr/bin/env python3
"""Funniest Forecast for a City That Isn't.

Writes one line, at most 120 characters: the funniest weather forecast
for a city that does not exist. The program writes the forecast to
``<MAKEFUN_OUTPUT_DIR>/entry.txt`` (default ``/output``), the path the
make.fun program/v1 harness grades.

The forecast (see CANDIDATES.md for the ten candidates and why this one
was picked): Drizzleford's rain falls sideways, and by Friday it turns
upward. The weather itself is the joke; the bulletin stays flat.

Standard library only: the grader installs nothing.
"""

import hashlib
import os
import sys

FORECAST = (
    "Drizzleford: rain falling sideways since Tuesday. "
    "Expect continued sideways rain, turning upward by Friday."
)

MAX_CHARS = 120


def output_dir() -> str:
    """Directory the harness wants the entry written to."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def entry_path() -> str:
    return os.path.join(output_dir(), "entry.txt")


def write_entry() -> str:
    """Write the forecast and return the path written."""
    text = FORECAST
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit(
            "forecast must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    if not text.strip():
        raise SystemExit("forecast must not be only whitespace")
    path = entry_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    return path


def check_entry() -> int:
    """Verify the written entry by reading it back and hashing it.

    Prints the character count and the SHA-256 of the file on disk, and
    exits 0 only when the file matches FORECAST exactly. The entry must
    also be exactly one line: a stray newline would count against the
    120-character gate and break the one-line format the judge reads.
    """
    path = entry_path()
    with open(path, "rb") as handle:
        raw = handle.read()
    text = raw.decode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    print("path: %s" % path)
    print("chars: %d" % len(text))
    print("sha256: %s" % digest)
    if text != FORECAST:
        print("MISMATCH: entry.txt does not equal FORECAST", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("MISMATCH: entry must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= MAX_CHARS:
        print("MISMATCH: length outside 1-%d" % MAX_CHARS, file=sys.stderr)
        return 1
    print("OK: entry matches FORECAST")
    return 0


def main(argv) -> int:
    if "--check" in argv:
        return check_entry()
    path = write_entry()
    print("wrote %s (%d chars)" % (path, len(FORECAST)))
    # Verify the write by reading it back before reporting success, so
    # a partial or corrupted write fails loudly instead of shipping.
    return check_entry()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

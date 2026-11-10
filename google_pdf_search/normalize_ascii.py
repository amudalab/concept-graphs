#!/usr/bin/env python3
"""Normalize transcript text files to ASCII-ish form."""

from __future__ import annotations

import argparse
import codecs
import unicodedata
from pathlib import Path


def normalize_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    path.write_text(ascii_text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory",
        nargs="?",
        default="data",
        type=Path,
        help="Directory of .txt files to normalize",
    )
    parser.add_argument(
        "--progress",
        type=Path,
        default=Path("data/txt2ascii.txt"),
        help="File listing already-processed names",
    )
    args = parser.parse_args(argv)

    done = set()
    if args.progress.exists():
        done = {
            line.strip()
            for line in args.progress.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    updated: list[str] = []
    for path in sorted(args.directory.glob("*.txt")):
        if path.name in done:
            continue
        normalize_file(path)
        updated.append(path.name)
        print(path.name)

    if updated:
        args.progress.write_text(
            "\n".join(sorted(done | set(updated))) + "\n", encoding="utf-8"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

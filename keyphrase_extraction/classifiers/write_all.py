#!/usr/bin/env python3
"""Concatenate per-lecture feature tables into a training dataset."""
from __future__ import annotations

import argparse
from pathlib import Path

from _internal.paths import KEYS_DIR, OUTPUT_DIR, TRAINING_DATA_DIR


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tab_files", help="Comma-separated lecture .tab names")
    parser.add_argument("output_file", help="Destination training .tab name")
    parser.add_argument("input_folder", nargs="?", default=str(OUTPUT_DIR))
    parser.add_argument("keys_folder", nargs="?", default=str(KEYS_DIR))
    parser.add_argument("output_folder", nargs="?", default=str(TRAINING_DATA_DIR))
    parser.add_argument("stemmer", nargs="?", default="none")
    args = parser.parse_args(argv)

    input_dir = Path(args.input_folder)
    output_dir = Path(args.output_folder)
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / args.output_file

    header_written = False
    with destination.open("w", encoding="utf-8") as out:
        for name in args.tab_files.split(","):
            path = input_dir / name.strip()
            if not path.exists():
                print(f"missing {path}")
                continue
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            if not header_written and lines:
                out.write("\n".join(lines[:3]) + "\n")
                header_written = True
            for line in lines[3:]:
                out.write(line + "\n")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Hand each new transcript to the keyphrase pipeline."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path("data"))
    parser.add_argument(
        "--progress",
        type=Path,
        default=Path("data/txt2keyphrase.txt"),
    )
    parser.add_argument(
        "--pipeline-script",
        type=Path,
        default=Path("../keyphrase_extraction/scripts/ss2.sh"),
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
            print(f"already processed: {path.name}")
            continue
        command = ["sh", str(args.pipeline_script), str(path)]
        print(" ".join(command))
        subprocess.run(command, check=False)
        updated.append(path.name)

    if updated:
        args.progress.write_text(
            "\n".join(sorted(done | set(updated))) + "\n", encoding="utf-8"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Batch-run the keyphrase pipeline over every transcript in data/transcripts.

Formerly ``fast_keyphrase_extraction/automate.py``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Reuse the canonical implementation from keyphrase_extraction.
from pipeline import run_pipeline  # noqa: E402
from _internal.paths import TRANSCRIPTS_DIR  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stemmer", default="none")
    parser.add_argument("--max-gram", type=int, default=3)
    parser.add_argument(
        "--skip-file",
        type=Path,
        default=Path("data/txt2keyphrase.txt"),
        help="Newline-separated list of already-processed filenames",
    )
    args = parser.parse_args(argv)

    skip = set()
    if args.skip_file.exists():
        skip = {
            line.strip()
            for line in args.skip_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    # Prefer local data/transcripts; fall back to shared module transcripts.
    local_transcripts = Path("data/transcripts")
    transcript_dir = local_transcripts if local_transcripts.exists() else TRANSCRIPTS_DIR

    processed: list[str] = []
    for path in sorted(transcript_dir.glob("*.txt")):
        if path.name in skip:
            continue
        print(f"==> {path.name}")
        run_pipeline(
            path.name,
            stemmer=args.stemmer,
            max_gram=args.max_gram,
            enable_pos=True,
        )
        processed.append(path.name)

    if processed:
        args.skip_file.parent.mkdir(parents=True, exist_ok=True)
        existing = sorted(skip | set(processed))
        args.skip_file.write_text("\n".join(existing) + "\n", encoding="utf-8")
    print(f"Processed {len(processed)} transcripts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Stem slide text dumps under data/video_text_slides."""
from __future__ import annotations

import argparse
from pathlib import Path

from _internal.paths import OUTPUT_DIR, VIDEO_SLIDES_DIR, lecture_stem
from _internal.stemming import parse_stemmer_name, stem_phrase


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lecture")
    parser.add_argument("stemmer")
    args = parser.parse_args(argv)
    stem = lecture_stem(args.lecture)
    name = parse_stemmer_name(args.stemmer)
    source_dir = VIDEO_SLIDES_DIR / stem
    dest_dir = OUTPUT_DIR / f"{stem}_slides"
    dest_dir.mkdir(parents=True, exist_ok=True)
    if not source_dir.is_dir():
        print(f"missing slides: {source_dir}")
        return 1
    for path in sorted(source_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8", errors="replace")
        stemmed = "\n".join(stem_phrase(line, name) for line in text.splitlines())
        (dest_dir / path.name).write_text(stemmed + "\n", encoding="utf-8")
    print(dest_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

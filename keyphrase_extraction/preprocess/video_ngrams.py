#!/usr/bin/env python3
"""Extract n-grams from stemmed slide text."""
from __future__ import annotations

import argparse

from lexicons.stopwords import stemmed_stopwords
from preprocess.ngrams import extract_ngrams
from _internal.io import write_lines
from _internal.paths import OUTPUT_DIR, lecture_stem
from _internal.stemming import parse_stemmer_name


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lecture")
    parser.add_argument("max_gram", type=int)
    parser.add_argument("stemmer", nargs="?", default="none")
    args = parser.parse_args(argv)
    stem = lecture_stem(args.lecture)
    name = parse_stemmer_name(args.stemmer)
    slide_dir = OUTPUT_DIR / f"{stem}_slides"
    tokens: list[str] = []
    if slide_dir.is_dir():
        for path in sorted(slide_dir.glob("*.txt")):
            tokens.extend(path.read_text(encoding="utf-8", errors="replace").split())
    tagged = [f"{tok}/NONE/{tok}" for tok in tokens]
    grams = extract_ngrams(
        tagged,
        max_gram=args.max_gram,
        stopwords=stemmed_stopwords(name),
    )
    dest = OUTPUT_DIR / f"{stem}_vgrams.txt"
    write_lines(dest, sorted(grams))
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

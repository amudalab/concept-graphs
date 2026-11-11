"""Video-slide occurrence features for candidate phrases."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Sequence

from _internal.io import read_lines, write_score_file
from _internal.paths import OUTPUT_DIR, VIDEO_SLIDES_DIR, lecture_stem


def _slide_texts(lecture_dir: Path) -> List[str]:
    if not lecture_dir.is_dir():
        return []
    texts: List[str] = []
    for path in sorted(lecture_dir.iterdir()):
        if path.suffix.lower() == ".txt":
            texts.append(path.read_text(encoding="utf-8", errors="replace").lower())
    return texts


def contiguous_count_ratio(
    grams: Sequence[str], slides: Sequence[str]
) -> Dict[str, float]:
    """Fraction of slides that contain each gram."""
    if not slides:
        return {gram: 0.0 for gram in grams}
    total = float(len(slides))
    return {
        gram: sum(1 for slide in slides if gram.lower() in slide) / total
        for gram in grams
    }


def frequency_occurrence_ratio(
    grams: Sequence[str], slides: Sequence[str]
) -> Dict[str, float]:
    """Mean per-slide occurrence count for each gram."""
    if not slides:
        return {gram: 0.0 for gram in grams}
    total = float(len(slides))
    return {
        gram: sum(slide.count(gram.lower()) for slide in slides) / total
        for gram in grams
    }


def score_contiguous(lecture: str, *, output_dir: Path = OUTPUT_DIR) -> Path:
    stem = lecture_stem(lecture)
    grams = read_lines(output_dir / f"{stem}_vgrams.txt") or read_lines(
        output_dir / f"{stem}_grams.txt"
    )
    slides = _slide_texts(VIDEO_SLIDES_DIR / stem)
    destination = output_dir / f"{stem}_cont.txt"
    write_score_file(destination, contiguous_count_ratio(grams, slides))
    return destination


def score_frequency(lecture: str, *, output_dir: Path = OUTPUT_DIR) -> Path:
    stem = lecture_stem(lecture)
    grams = read_lines(output_dir / f"{stem}_vgrams.txt") or read_lines(
        output_dir / f"{stem}_grams.txt"
    )
    slides = _slide_texts(VIDEO_SLIDES_DIR / stem)
    destination = output_dir / f"{stem}_freq.txt"
    write_score_file(destination, frequency_occurrence_ratio(grams, slides))
    return destination


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        choices=("contiguous", "frequency", "cont", "freq"),
        nargs="?",
        default="contiguous",
        help="Which slide-occurrence feature to compute",
    )
    parser.add_argument("lecture")
    parser.add_argument("ext", nargs="?", default=None)
    args = parser.parse_args(argv)
    if args.mode in {"frequency", "freq"}:
        print(score_frequency(args.lecture))
    else:
        print(score_contiguous(args.lecture))
    return 0


# Backward-compatible aliases for older callers.
main_contiguous = main
main_frequency = main


if __name__ == "__main__":
    raise SystemExit(main())

"""Dispersion via Fano factor over fixed-size windows."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np

from _internal.io import read_lines, write_score_file
from _internal.paths import OUTPUT_DIR, lecture_stem


def _fano_frequencies(
    positions: Sequence[int], window_count: int, window_size: int
) -> List[int]:
    frequencies: List[int] = []
    cursor = 0
    for start in range(0, window_count * window_size - window_size, window_size):
        end = start + window_size
        if cursor < len(positions) and start < positions[cursor] <= end:
            count = 0
            while cursor < len(positions) and positions[cursor] <= end:
                cursor += 1
                count += 1
            frequencies.append(count)
        else:
            frequencies.append(0)
    return frequencies


def _dispersion_from_fano(frequencies: Sequence[int]) -> float:
    if not frequencies:
        return 0.0
    values = np.asarray(frequencies, dtype=float)
    variance = float(np.var(values))
    mean = float(np.mean(values))
    if variance + mean == 0:
        return 0.0
    return mean / (variance + mean)


def _phrase_positions(tokens: Sequence[str], phrase: str) -> List[int]:
    parts = phrase.split()
    width = len(parts)
    if width == 0:
        return []
    positions: List[int] = []
    for index in range(0, len(tokens) - width + 1):
        if tokens[index : index + width] == parts:
            positions.append(index + 1)
    return positions


def dispersion_scores(
    tokens: Sequence[str],
    phrases: Sequence[str],
    *,
    window_size: int,
    min_occurrences: int,
) -> Dict[str, float]:
    window_count = len(tokens) // window_size
    if len(tokens) % window_size:
        window_count += 1

    scores: Dict[str, float] = {}
    for phrase in phrases:
        positions = _phrase_positions(tokens, phrase)
        if len(positions) <= min_occurrences:
            scores[phrase] = 0.0
        else:
            scores[phrase] = _dispersion_from_fano(
                _fano_frequencies(positions, window_count, window_size)
            )
    return scores


def score_file(
    lecture: str,
    *,
    window_size: int = 60,
    min_occurrences: int = 0,
    output_dir: Path = OUTPUT_DIR,
    grams_ext: str = "_grams.txt",
    untagged_ext: str = "_untagged.txt",
    result_ext: str = "_disp.txt",
) -> Path:
    stem = lecture_stem(lecture)
    tokens = (
        (output_dir / f"{stem}{untagged_ext}")
        .read_text(encoding="utf-8", errors="replace")
        .split()
    )
    phrases = read_lines(output_dir / f"{stem}{grams_ext}")
    scores = dispersion_scores(
        tokens, phrases, window_size=window_size, min_occurrences=min_occurrences
    )
    destination = output_dir / f"{stem}{result_ext}"
    write_score_file(destination, scores)
    return destination


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute dispersion feature scores.")
    parser.add_argument("lecture")
    parser.add_argument("window_size", nargs="?", type=int, default=60)
    parser.add_argument("stemmer", nargs="?", default="none")
    args = parser.parse_args(argv)
    print(score_file(args.lecture, window_size=args.window_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

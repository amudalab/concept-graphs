"""Candidate phrase C-score (length-weighted frequency with subsumption)."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence

from _internal.io import read_lines, write_score_file
from _internal.paths import OUTPUT_DIR, lecture_stem
from _internal.text import contains_as_phrase


class CScoreExtractor:
    """Compute C-scores for a set of candidate grams in a transcript."""

    def __init__(self, transcript: str, grams: Sequence[str]) -> None:
        self._transcript = transcript
        self._grams = [gram for gram in grams if gram.strip()]
        self._max_length = max((len(gram.split()) for gram in self._grams), default=0)
        self._frequencies: Dict[str, int] = {
            gram: transcript.count(gram) for gram in self._grams
        }

    def scores(self) -> Dict[str, float]:
        result: Dict[str, float] = {}
        for gram in self._grams:
            length = len(gram.split())
            if length == 0:
                continue
            frequency = self._frequencies[gram]
            if length == self._max_length:
                result[gram] = math.log(length, 2) * frequency
                continue

            parents = [
                other
                for other in self._grams
                if other != gram
                and len(other.split()) > length
                and contains_as_phrase(gram, other)
            ]
            if parents:
                parent_freq = sum(self._frequencies[parent] for parent in parents) / len(
                    parents
                )
                result[gram] = math.log(length, 2) * (frequency - parent_freq)
            else:
                result[gram] = math.log(length, 2) * frequency
        return result


def score_file(
    lecture: str,
    *,
    output_dir: Path = OUTPUT_DIR,
    grams_ext: str = "_grams.txt",
    untagged_ext: str = "_untagged.txt",
    result_ext: str = "_cscore.txt",
    grams: Sequence[str] | None = None,
) -> Path:
    """Score grams for one lecture and write ``{lecture}_cscore.txt``."""
    stem = lecture_stem(lecture)
    transcript_path = output_dir / f"{stem}{untagged_ext}"
    gram_list = (
        list(grams)
        if grams is not None
        else read_lines(output_dir / f"{stem}{grams_ext}")
    )
    transcript = transcript_path.read_text(encoding="utf-8", errors="replace")
    scores = CScoreExtractor(transcript, gram_list).scores()
    destination = output_dir / f"{stem}{result_ext}"
    write_score_file(destination, scores)
    return destination


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute C-scores for candidate grams.")
    parser.add_argument("lecture", help="Lecture filename or stem (e.g. ds1.txt)")
    parser.add_argument(
        "stemmer",
        nargs="?",
        default="none",
        help="Accepted for CLI compatibility; C-score itself does not stem.",
    )
    args = parser.parse_args(argv)
    path = score_file(args.lecture)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

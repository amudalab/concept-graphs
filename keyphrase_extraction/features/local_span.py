"""Local-span feature: how unevenly a phrase is distributed across segments."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Sequence

from _internal.io import read_lines, write_score_file
from _internal.paths import OUTPUT_DIR, lecture_stem


class LocalSpanExtractor:
    """Score candidate grams by peak deviation from their per-segment average."""

    def __init__(
        self,
        tokens: Sequence[str],
        grams: Sequence[str],
        *,
        segment_count: int = 5,
    ) -> None:
        self._tokens = list(tokens)
        self._text = " ".join(self._tokens)
        self._grams = [gram.lower() for gram in grams if gram.strip()]
        self._segment_count = segment_count
        self._segment_size = len(self._tokens) // segment_count if segment_count else 0

    def scores(self) -> Dict[str, float]:
        if self._segment_size <= 0:
            return {}

        result: Dict[str, float] = {}
        for gram in self._grams:
            if len(gram.split()) <= 1:
                continue
            total = self._text.count(gram)
            if total <= 2:
                continue
            average = total / float(self._segment_count)
            deviations: List[float] = []
            for segment_index in range(self._segment_count):
                start = segment_index * self._segment_size
                end = start + self._segment_size
                primary = " ".join(self._tokens[start:end])
                deviations.append(abs(primary.count(gram) - average))

                half = start + self._segment_size // 2
                overlap_end = min(end, len(self._tokens))
                overlap = " ".join(self._tokens[half:overlap_end])
                # Match legacy behaviour: accumulate onto the same string then recount.
                combined = primary + " " + overlap
                deviations.append(abs(combined.count(gram) - average))
            result[gram] = max(deviations) if deviations else 0.0
        return result


def score_file(
    lecture: str,
    *,
    output_dir: Path = OUTPUT_DIR,
    grams_ext: str = "_grams.txt",
    untagged_ext: str = "_untagged.txt",
    result_ext: str = "_localspan.txt",
) -> Path:
    stem = lecture_stem(lecture)
    tokens = (
        (output_dir / f"{stem}{untagged_ext}")
        .read_text(encoding="utf-8", errors="replace")
        .lower()
        .split()
    )
    grams = read_lines(output_dir / f"{stem}{grams_ext}")
    scores = LocalSpanExtractor(tokens, grams).scores()
    destination = output_dir / f"{stem}{result_ext}"
    write_score_file(destination, scores)
    return destination


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute local-span feature scores.")
    parser.add_argument("lecture")
    parser.add_argument("max_gram", nargs="?", default="3")
    parser.add_argument("stemmer", nargs="?", default="none")
    args = parser.parse_args(argv)
    print(score_file(args.lecture))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

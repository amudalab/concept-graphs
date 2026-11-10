"""Cue-phrase feature: extract definitions following spoken cue patterns."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from lexicons.cue_phrases import stemmed_cue_phrases
from lexicons.stopwords import stemmed_stopwords
from _internal.io import write_score_file
from _internal.paths import OUTPUT_DIR, lecture_stem
from _internal.stemming import StemmerName, parse_stemmer_name
from _internal.text import BOUNDARY_STOPWORDS, strip_boundary_stopwords


class CueFeatureExtractor:
    """Find candidate keyphrases that follow definitional cue phrases."""

    def __init__(
        self,
        tokens: Sequence[str],
        *,
        cue_phrases: Sequence[str],
        stopwords: Iterable[str],
        max_gram: int = 3,
        window: int = 5,
    ) -> None:
        self._tokens = list(tokens)
        self._cue_phrases = list(cue_phrases)
        self._stopwords = set(stopwords)
        self._max_gram = max_gram
        self._window = window
        self._candidates: List[str] = []

    def extract(self) -> Dict[str, float]:
        self._candidates.clear()
        token_count = len(self._tokens)
        for index in range(token_count):
            matched = self._match_cue_at(index)
            if matched is None:
                continue
            cue_length, _cue = matched
            start = index + cue_length
            window_tokens = self._tokens[start : start + self._window]
            if not window_tokens:
                continue
            phrase = self._candidate_from_window(window_tokens)
            if phrase and phrase not in self._candidates and phrase not in BOUNDARY_STOPWORDS:
                self._candidates.append(phrase)

        # Legacy behaviour: presence indicator (1) rather than true frequency.
        return {phrase: 1.0 for phrase in self._candidates}

    def _match_cue_at(self, index: int) -> tuple[int, str] | None:
        for cue in self._cue_phrases:
            cue_tokens = cue.split()
            end = index + len(cue_tokens)
            if end > len(self._tokens):
                continue
            if self._tokens[index:end] == cue_tokens:
                return len(cue_tokens), cue
        return None

    def _candidate_from_window(self, window_tokens: Sequence[str]) -> str:
        collected: List[str] = []
        for token in window_tokens:
            if token in self._stopwords:
                break
            collected.append(token)
        phrase = strip_boundary_stopwords(" ".join(collected))
        if len(phrase.split()) <= 1:
            return ""
        return phrase


def score_file(
    lecture: str,
    stemmer_name: str | StemmerName,
    max_gram: int,
    *,
    output_dir: Path = OUTPUT_DIR,
    untagged_ext: str = "_untagged.txt",
    result_ext: str = "_cue.txt",
) -> Path:
    stem = lecture_stem(lecture)
    transcript_path = output_dir / f"{stem}{untagged_ext}"
    tokens = transcript_path.read_text(encoding="utf-8", errors="replace").split()
    name = parse_stemmer_name(stemmer_name) if isinstance(stemmer_name, str) else stemmer_name
    scores = CueFeatureExtractor(
        tokens,
        cue_phrases=stemmed_cue_phrases(name),
        stopwords=stemmed_stopwords(name),
        max_gram=max_gram,
    ).extract()
    destination = output_dir / f"{stem}{result_ext}"
    write_score_file(destination, scores)
    return destination


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract cue-phrase keyphrase features.")
    parser.add_argument("lecture", help="Lecture filename or stem")
    parser.add_argument("stemmer", help="Porter-Stemmer | Lancaster-Stemmer | WordNet-Lemmatizer | none")
    parser.add_argument("max_gram", type=int, help="Maximum cue length considered")
    args = parser.parse_args(argv)
    print(score_file(args.lecture, args.stemmer, args.max_gram))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

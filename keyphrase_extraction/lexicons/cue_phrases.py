"""Cue-phrase lexicon loaded from ``config/cue_phrases.txt``."""

from __future__ import annotations

from functools import lru_cache
from typing import FrozenSet, List

from _internal.paths import CONFIG_DIR
from _internal.stemming import StemmerName, stem_phrase


@lru_cache(maxsize=1)
def load_cue_phrases() -> FrozenSet[str]:
    path = CONFIG_DIR / "cue_phrases.txt"
    return frozenset(
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )


def stemmed_cue_phrases(stemmer_name: StemmerName | str) -> List[str]:
    """Return cue phrases longest-first so greedy matching prefers longer cues."""
    phrases = [stem_phrase(phrase, stemmer_name) for phrase in load_cue_phrases()]
    return sorted(set(phrases), key=len, reverse=True)

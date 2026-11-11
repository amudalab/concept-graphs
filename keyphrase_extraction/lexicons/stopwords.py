"""Stopword lexicon loaded from ``config/stopwords.txt``."""

from __future__ import annotations

from functools import lru_cache
from typing import FrozenSet

from _internal.paths import CONFIG_DIR
from _internal.stemming import StemmerName, stem_sequence


@lru_cache(maxsize=1)
def load_stopwords() -> FrozenSet[str]:
    path = CONFIG_DIR / "stopwords.txt"
    return frozenset(
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )


def stemmed_stopwords(stemmer_name: StemmerName | str) -> FrozenSet[str]:
    return frozenset(stem_sequence(sorted(load_stopwords()), stemmer_name))

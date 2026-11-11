"""Stemming / lemmatization helpers."""

from __future__ import annotations

from enum import Enum
from functools import lru_cache
from typing import Callable, Iterable, List, Sequence

from nltk import stem


class StemmerName(str, Enum):
    NONE = "none"
    PORTER = "Porter-Stemmer"
    LANCASTER = "Lancaster-Stemmer"
    WORDNET = "WordNet-Lemmatizer"


def parse_stemmer_name(value: str) -> StemmerName:
    normalized = value.strip()
    if normalized.lower() in {"", "none", "null"}:
        return StemmerName.NONE
    try:
        return StemmerName(normalized)
    except ValueError as exc:
        raise ValueError(
            f"Unknown stemmer {value!r}. "
            f"Expected one of: {[s.value for s in StemmerName]}"
        ) from exc


@lru_cache(maxsize=8)
def _token_transform(stemmer_name: StemmerName) -> Callable[[str], str]:
    if stemmer_name is StemmerName.NONE:
        return lambda token: token
    if stemmer_name is StemmerName.PORTER:
        porter = stem.PorterStemmer()
        return porter.stem
    if stemmer_name is StemmerName.LANCASTER:
        lancaster = stem.LancasterStemmer()
        return lancaster.stem
    if stemmer_name is StemmerName.WORDNET:
        lemmatizer = stem.WordNetLemmatizer()
        return lemmatizer.lemmatize
    raise ValueError(f"Unsupported stemmer: {stemmer_name}")


def stem_token(token: str, stemmer_name: StemmerName | str) -> str:
    """Stem or lemmatize a single token."""
    name = (
        stemmer_name
        if isinstance(stemmer_name, StemmerName)
        else parse_stemmer_name(stemmer_name)
    )
    return _token_transform(name)(token)


def stem_phrase(phrase: str, stemmer_name: StemmerName | str) -> str:
    """Stem each whitespace-separated token in a phrase."""
    name = (
        stemmer_name
        if isinstance(stemmer_name, StemmerName)
        else parse_stemmer_name(stemmer_name)
    )
    transform = _token_transform(name)
    return " ".join(transform(token) for token in phrase.split())


def stem_sequence(
    words: Sequence[str], stemmer_name: StemmerName | str
) -> List[str]:
    """Return a new list with each word stemmed."""
    name = (
        stemmer_name
        if isinstance(stemmer_name, StemmerName)
        else parse_stemmer_name(stemmer_name)
    )
    transform = _token_transform(name)
    return [transform(word) for word in words]


def stem_inplace(words: List[str], stemmer_name: StemmerName | str) -> List[str]:
    """Stem words in place and return the same list (legacy-compatible)."""
    stemmed = stem_sequence(words, stemmer_name)
    words[:] = stemmed
    return words

"""Small text helpers used across feature extractors."""

from __future__ import annotations

import re
from typing import Iterable, Set

_PUNCT_STRIP = str.maketrans("", "", ".,:;!?()[]{}\"'`-")

BOUNDARY_STOPWORDS: frozenset[str] = frozenset(
    {"of", "a", "an", "the", "and", "or"}
)


def is_number(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def clean_token(token: str) -> str:
    """Lowercase and strip common punctuation from a token."""
    return token.lower().translate(_PUNCT_STRIP).strip()


def clean_phrase(phrase: str) -> str:
    return " ".join(clean_token(token) for token in phrase.split() if clean_token(token))


def strip_boundary_stopwords(phrase: str, stopwords: Iterable[str] | None = None) -> str:
    """Remove leading/trailing function words from a candidate phrase."""
    banned: Set[str] = set(stopwords) if stopwords is not None else set(BOUNDARY_STOPWORDS)
    tokens = phrase.split()
    while tokens and tokens[0] in banned:
        tokens.pop(0)
    while tokens and tokens[-1] in banned:
        tokens.pop()
    return " ".join(tokens)


def contains_as_phrase(needle: str, haystack: str) -> bool:
    """True when ``needle`` appears as a whole word/phrase inside ``haystack``."""
    return f" {needle} " in f" {haystack} "


_TAGGED_TOKEN = re.compile(r"^([^/]+)/")


def surface_from_tagged(token: str) -> str:
    """Extract the surface form from an ``word/POS/lemma`` style token."""
    match = _TAGGED_TOKEN.match(token)
    return match.group(1) if match else token

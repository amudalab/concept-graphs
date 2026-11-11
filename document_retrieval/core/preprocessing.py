"""Preprocessing helpers: stopword removal and lemmatisation."""

from __future__ import annotations

from typing import Iterable


def remove_stopword(tokens: Iterable[str]) -> list[str]:
    """Return tokens that are neither English stopwords nor 3 characters or fewer."""
    from nltk.corpus import stopwords

    stopset = set(stopwords.words("english"))
    return [word for word in tokens if word.lower() not in stopset and len(word) > 3]


def lemmatize_words(words: Iterable[str]) -> list[str]:
    """Return the WordNet lemma of each word."""
    from nltk.stem import WordNetLemmatizer

    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words]

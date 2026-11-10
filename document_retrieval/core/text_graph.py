"""Build term graphs from a list of keyphrases and a source document.

``create_graph`` finds where each keyphrase occurs in the document, resolves
overlapping phrases (``"linked"`` vs ``"linked list"``), and builds an
:class:`adjmatrix.AdjMatrix` of word distances.  ``update_graph`` performs the
same position analysis for an additional document without building a matrix.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Sequence

import nltk

from core.adjacency import AdjMatrix, PositionList

if TYPE_CHECKING:
    from textmodel import Text

_TOKEN_PATTERN = r"[\w']+"

# (term, token index in the document)
Position = tuple[str, int]


def create_graph(text: Text, filename: str | Path) -> AdjMatrix:
    """Create the word graph for ``text.tokens`` over the document ``filename``.

    ``text.tokens`` is replaced by the sorted list of terms that actually
    occur in the document.
    """
    terms, merged_positions = _collect_term_positions(text, filename)
    matrix = AdjMatrix()
    matrix.create_matrix(terms, merged_positions, False)
    return matrix


def update_graph(text: Text, filename: str | Path) -> list[Position]:
    """Find term positions for another document and return them in order.

    ``text.tokens`` is replaced by the sorted list of terms that occur in the
    document.  The returned list is suitable for
    :meth:`adjmatrix.AdjMatrix.update_matrix`.
    """
    _, merged_positions = _collect_term_positions(text, filename)
    return merged_positions


def find_word_positions(
    document_tokens: Sequence[str], word: str, known_terms: Sequence[str]
) -> list[Position]:
    """Return ``(term, index)`` for each occurrence of ``word`` in the document."""
    positions: list[Position] = []
    for index, token in enumerate(document_tokens):
        if token != word:
            continue
        term = word
        spaced = term.replace("-", " ")
        if spaced in known_terms:
            if spaced.endswith("s") and spaced[:-1] in known_terms:
                term = spaced[:-1]
            else:
                term = spaced
        positions.append((term, index))
    return positions


def find_phrase_positions(
    document_tokens: Sequence[str], phrase: str, known_terms: Sequence[str]
) -> list[Position]:
    """Return ``(term, index)`` for each occurrence of ``phrase`` in the document.

    The last word of the phrase is compared ignoring a plural ``s``.  A phrase
    that would end exactly on the last document token is not matched.
    """
    phrase_tokens = nltk.regexp_tokenize(phrase, _TOKEN_PATTERN)
    positions: list[Position] = []
    if not phrase_tokens:
        return positions
    for index, token in enumerate(document_tokens):
        if token != phrase_tokens[0]:
            continue
        if index + len(phrase_tokens) >= len(document_tokens):
            continue
        candidate = list(document_tokens[index : index + len(phrase_tokens)])
        if not _phrases_match(phrase_tokens, candidate):
            continue
        term = phrase
        spaced = term.replace("-", " ")
        if spaced in known_terms or spaced[:-1] in known_terms:
            if spaced.endswith("s") and spaced[:-1] in known_terms:
                term = spaced[:-1]
            else:
                term = spaced
        if term.endswith("s") and term[:-1] in known_terms:
            term = term[:-1]
        positions.append((term, index))
    return positions


def _collect_term_positions(
    text: Text, filename: str | Path
) -> tuple[list[str], list[Position]]:
    """Locate ``text.tokens`` in ``filename`` and prune overlapping terms.

    Updates ``text.tokens`` in place and returns ``(terms, merged_positions)``
    where ``terms`` is the sorted list of surviving terms.
    """
    # Corpus files are not guaranteed to be valid UTF-8.
    document = Path(filename).read_text(encoding="utf-8", errors="replace").lower()
    document_tokens = nltk.regexp_tokenize(document, _TOKEN_PATTERN)

    terms = list(text.tokens)
    positions_by_term: dict[str, list[Position]] = {}
    unmatched_or_renamed: list[str] = []

    for term in terms:
        term_tokens = nltk.regexp_tokenize(term, _TOKEN_PATTERN)
        if len(term_tokens) == 1:
            positions = find_word_positions(document_tokens, term_tokens[0], terms)
        elif len(term_tokens) > 1:
            positions = find_phrase_positions(document_tokens, term, terms)
        else:
            positions = []
            unmatched_or_renamed.append(term)
        if positions:
            canonical = positions[0][0]
            if canonical in positions_by_term:
                for position in positions:
                    if position not in positions_by_term[canonical]:
                        positions_by_term[canonical].append(position)
            else:
                positions_by_term[canonical] = positions
            if canonical != term:
                unmatched_or_renamed.append(term)

    _drop_subphrases_with_same_count(positions_by_term, terms)
    _drop_fully_covered_terms(positions_by_term, terms)

    for term in unmatched_or_renamed:
        terms.remove(term)

    position_lists = list(positions_by_term.values())
    merged = _merge_position_lists(position_lists)

    seen_terms = {term for term, _ in merged}
    for term in [t for t in terms if t not in seen_terms]:
        terms.remove(term)

    terms.sort()
    text.tokens = terms
    return terms, merged


def _drop_subphrases_with_same_count(
    positions_by_term: dict[str, list[Position]], terms: list[str]
) -> None:
    """Remove ``x`` when a longer phrase ``y`` contains it and occurs as often."""
    removable: list[str] = []
    for short_term in positions_by_term:
        for long_term in positions_by_term:
            if short_term == long_term or short_term not in long_term:
                continue
            if not _is_token_subsequence(
                nltk.word_tokenize(short_term), nltk.word_tokenize(long_term)
            ):
                continue
            same_count = len(positions_by_term[short_term]) == len(
                positions_by_term[long_term]
            )
            if same_count and short_term not in removable:
                removable.append(short_term)
    for term in removable:
        del positions_by_term[term]
        terms.remove(term)


def _drop_fully_covered_terms(
    positions_by_term: dict[str, list[Position]], terms: list[str]
) -> None:
    """Remove terms whose occurrences are all inside longer matched phrases."""
    remaining = {term: len(positions) for term, positions in positions_by_term.items()}
    # Multi-word terms are processed first, then single-word terms.
    for want_multiword in (True, False):
        for term in positions_by_term:
            word_count = len(nltk.word_tokenize(term))
            if want_multiword and word_count <= 1:
                continue
            if not want_multiword and word_count != 1:
                continue
            for other in positions_by_term:
                if term != other and term in other:
                    remaining[term] -= remaining[other]
    for term in [t for t in positions_by_term if remaining[t] == 0]:
        terms.remove(term)
        del positions_by_term[term]


def _is_token_subsequence(
    needle_tokens: Sequence[str], haystack_tokens: Sequence[str]
) -> bool:
    """Return True if ``needle_tokens`` appear in order within ``haystack_tokens``."""
    matched = 0
    for token in haystack_tokens:
        if matched == len(needle_tokens):
            break
        if token == needle_tokens[matched]:
            matched += 1
    return matched == len(needle_tokens)


def _stem_plural(word: str) -> str:
    return word.removesuffix("s")


def _phrases_match(phrase_tokens: Sequence[str], candidate_tokens: Sequence[str]) -> bool:
    """Return True if the candidate equals the phrase, ignoring a plural last word."""
    if len(phrase_tokens) < 2:
        return False
    if list(phrase_tokens[:-1]) != list(candidate_tokens[:-1]):
        return False
    return _stem_plural(phrase_tokens[-1]) == _stem_plural(candidate_tokens[-1])


def _merge_position_lists(position_lists: list[list[Position]]) -> list[Position]:
    """Merge the per-term position lists into one list ordered by token index.

    Fewer than two lists yields an empty result, as in the original pipeline.
    """
    merged: list[Position] = []
    if len(position_lists) > 1:
        merged = _merge_two(position_lists[0], position_lists[1])
    for position_list in position_lists[2:]:
        if position_list:
            merged = _merge_two(merged, position_list)
    return merged


def _merge_two(first: PositionList, second: PositionList) -> list[Position]:
    """Merge two position lists sorted by token index."""
    merged: list[Position] = []
    i = j = 0
    while i < len(first) and j < len(second):
        if first[i][1] < second[j][1]:
            merged.append(first[i])
            i += 1
        elif first[i][1] > second[j][1]:
            merged.append(second[j])
            j += 1
        else:
            merged.append(first[i])
            if first[i][0] != second[j][0]:
                merged.append(second[j])
            i += 1
            j += 1
    merged.extend(first[i:])
    merged.extend(second[j:])
    return merged

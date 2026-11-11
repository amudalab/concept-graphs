"""Helpers shared by the ``doc_ret_*`` retrieval variants (internal)."""

from __future__ import annotations

import math
import operator
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import core.graph_init as graph_init

KEYWORDS_PATH = Path("data/keywords")
FILEKEYS_PATH = Path("data/filekeys")
QUERY_KEY_PATH = Path("data/query.key")
QUERY_TEXT_PATH = Path("data/query.txt")

TOP_DOCUMENT_COUNT = 10

# Similarity credited to a term found in the 1st..4th importance cluster of a document.
_LEVEL_SIMILARITY = (1.0, 0.75, 0.5, 0.25)


@dataclass
class DocumentKeys:
    """Keyphrases of one document, as recorded in ``data/filekeys``."""

    name: str
    keys: list[str]
    level_texts: list[str]
    """Comma-joined keyphrases of each importance cluster, most important first."""


def load_keywords() -> list[str]:
    """Return the global keyword vocabulary from ``data/keywords``."""
    lines = KEYWORDS_PATH.read_text(encoding="utf-8").split("\n")
    return [line for line in lines if line]


def build_query_graph(query: str, *, write_query_text: bool = True) -> list[str]:
    """Write the query files, build the query's concept graph and return its terms.

    The graph itself is available afterwards from :func:`graph_init.get_matrix`.
    """
    if write_query_text:
        QUERY_TEXT_PATH.parent.mkdir(parents=True, exist_ok=True)
        QUERY_TEXT_PATH.write_text(query, encoding="utf-8")
    matched = [keyword for keyword in load_keywords() if keyword in query]
    QUERY_KEY_PATH.write_text("".join(f"{k}\n" for k in matched), encoding="utf-8")
    return graph_init.initgraph(QUERY_KEY_PATH, QUERY_TEXT_PATH)


def load_document_keys() -> dict[str, DocumentKeys]:
    """Parse ``data/filekeys`` (``name<<cluster<<cluster...``) by document name."""
    documents: dict[str, DocumentKeys] = {}
    for line in FILEKEYS_PATH.read_text(encoding="utf-8").split("\n"):
        if not line:
            continue
        clusters = line.split("<<")
        fields = line.replace("<<", ",").split(",")
        documents[fields[0]] = DocumentKeys(fields[0], fields[1:], clusters[1:])
    return documents


def rank_by_key_overlap(
    query_terms: Iterable[str], documents: Mapping[str, DocumentKeys]
) -> list[tuple[str, int]]:
    """Rank documents by how many query terms they share, most overlap first.

    Ties are listed in reverse file order.
    """
    query_set = set(query_terms)
    overlap = {name: len(query_set & set(doc.keys)) for name, doc in documents.items()}
    return sorted(overlap.items(), key=operator.itemgetter(1))[::-1]


def level_similarity(terms: Iterable[str], document: DocumentKeys) -> dict[str, float]:
    """Score each term by the importance cluster of ``document`` that mentions it.

    Cluster membership is a substring test against the cluster's comma-joined
    text, as in the original implementation.
    """
    similarity: dict[str, float] = {}
    for term in terms:
        score = 0.0
        for level_score, level_text in zip(_LEVEL_SIMILARITY, document.level_texts):
            if term in level_text:
                score = level_score
                break
        similarity[term] = score
    return similarity


def euclidean_distance(
    query_vector: Mapping[str, float], similarity: Mapping[str, float]
) -> float:
    """Distance between a query term vector and a document's term similarity."""
    total = 0.0
    for term, value in query_vector.items():
        total += (value - similarity.get(term, 0.0)) ** 2
    return math.sqrt(total)


def rank_by_vector_distance(
    query_vector: Mapping[str, float],
    query_terms: Sequence[str],
    documents: Mapping[str, DocumentKeys],
) -> list[tuple[str, float]]:
    """Rank the top documents by distance between ``query_vector`` and each document.

    The :data:`TOP_DOCUMENT_COUNT` documents sharing the most terms with the
    query are scored; the closest comes first.
    """
    distances: dict[str, float] = {}
    for name, _ in rank_by_key_overlap(query_terms, documents)[:TOP_DOCUMENT_COUNT]:
        document = documents[name]
        shared_terms = set(query_terms) & set(document.keys)
        similarity = level_similarity(shared_terms, document)
        distances[name] = euclidean_distance(query_vector, similarity)
    return sorted(distances.items(), key=operator.itemgetter(1))

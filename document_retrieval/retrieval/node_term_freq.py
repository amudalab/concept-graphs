"""Term-frequency document retrieval.

Each query term is weighted by its (normalised) frequency in the query text and
documents are ranked by distance to their per-cluster term similarities.
"""

from __future__ import annotations

import sys

from retrieval.common import (
    build_query_graph,
    load_document_keys,
    rank_by_vector_distance,
)


def retrieve_documents(query: str) -> list[str]:
    """Return document names ordered by closeness to the query's term frequencies."""
    query_terms = build_query_graph(query)
    if not query_terms:
        return []

    frequency = {term: query.count(term) for term in query_terms}
    max_frequency = max(frequency.values())
    if max_frequency == 0:
        return []
    # True division: frequencies are normalised into the range [0, 1].
    normalized_frequency = {
        term: count / max_frequency for term, count in frequency.items()
    }
    ranked = rank_by_vector_distance(
        normalized_frequency, query_terms, load_document_keys()
    )
    return [name for name, _ in ranked]


def main(argv: list[str] | None = None) -> None:
    arguments = sys.argv[1:] if argv is None else argv
    for name in retrieve_documents(" ".join(arguments)):
        print(name)


if __name__ == "__main__":
    main()

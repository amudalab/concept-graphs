"""Degree-based document retrieval.

Each query term is weighted by its (normalised) degree in the query graph and
documents are ranked by distance to their per-cluster term similarities.
"""

from __future__ import annotations

import sys

import core.graph_init as graph_init
from retrieval.common import (
    build_query_graph,
    load_document_keys,
    rank_by_vector_distance,
)


def rank_documents(query: str, *, write_query_text: bool = True) -> list[tuple[str, float]]:
    """Return ``(document, distance)`` pairs, closest document first."""
    query_terms = build_query_graph(query, write_query_text=write_query_text)
    if not query_terms:
        return []
    cells = graph_init.get_matrix().gmatrix

    degree = {
        term: float(
            sum(1 for other in query_terms if cells[term][other].weight != float("inf"))
        )
        for term in query_terms
    }
    max_degree = max(degree.values())
    if max_degree == 0:
        return []
    normalized_degree = {term: value / max_degree for term, value in degree.items()}
    return rank_by_vector_distance(normalized_degree, query_terms, load_document_keys())


def retrieve_documents(query: str) -> list[str]:
    """Return document names (without the ``.gdf`` suffix), closest first."""
    return [name[:-4] for name, _ in rank_documents(query)]


def main(argv: list[str] | None = None) -> None:
    arguments = sys.argv[1:] if argv is None else argv
    for name in retrieve_documents(" ".join(arguments)):
        print(name)


if __name__ == "__main__":
    main()

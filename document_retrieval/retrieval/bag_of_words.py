"""Bag-of-words document retrieval: rank documents by shared keyphrases."""

from __future__ import annotations

import sys

from retrieval.common import (
    TOP_DOCUMENT_COUNT,
    build_query_graph,
    load_document_keys,
    rank_by_key_overlap,
)


def retrieve_documents(query: str) -> list[str]:
    """Return the names of the documents sharing the most keyphrases with ``query``."""
    query_terms = build_query_graph(query)
    ranked = rank_by_key_overlap(query_terms, load_document_keys())
    return [name for name, _ in ranked[:TOP_DOCUMENT_COUNT]]


def main(argv: list[str] | None = None) -> None:
    arguments = sys.argv[1:] if argv is None else argv
    for name in retrieve_documents(" ".join(arguments)):
        print(name)


if __name__ == "__main__":
    main()

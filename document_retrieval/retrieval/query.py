"""CLI: degree-based retrieval for the query stored in ``data/query.txt``."""

from __future__ import annotations

from retrieval.common import QUERY_TEXT_PATH
from retrieval.node_degree import rank_documents


def main() -> None:
    query = QUERY_TEXT_PATH.read_text(encoding="utf-8").lower()
    for name, _ in rank_documents(query, write_query_text=False):
        print(name)


if __name__ == "__main__":
    main()

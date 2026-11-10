"""CLI: show how a document's concept clusters are ordered by average degree."""

from __future__ import annotations

import sys
from pathlib import Path

from taxonomy.taxonomy import order_clusters_by_average_degree, read_clusters

DEFAULT_WORKBOOK = Path("data/doc_details/ds2.xlsx")
CLUSTER_COUNT = 4


def main(argv: list[str] | None = None) -> None:
    arguments = sys.argv[1:] if argv is None else argv
    workbook_path = Path(arguments[0]) if arguments else DEFAULT_WORKBOOK
    clusters = read_clusters(
        workbook_path, CLUSTER_COUNT, all_sheets=False, with_degree=True
    )
    order = order_clusters_by_average_degree(clusters)
    for rank, cluster_index in enumerate(order):
        labels = ", ".join(entry.label for entry in clusters[cluster_index])
        print(f"{rank}: cluster {cluster_index}: {labels}")


if __name__ == "__main__":
    main()

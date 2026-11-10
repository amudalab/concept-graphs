"""Build per-document taxonomies and the ``data/filekeys`` retrieval index.

For every ``data/doc_graphs/<name>.gdf`` the cluster spreadsheet
``data/doc_details/<name>.xlsx`` is read, clusters are ordered by average
concept degree, a taxonomy is written to ``data/taxonomies/tax<name>.gdf`` and
one ``<name>.gdf<<cluster<<cluster...`` line is appended to ``data/filekeys``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from core.gdf_io import read_gdf
from taxonomy.taxonomy import (
    ClusterEntry,
    TaxonomyBuilder,
    order_clusters_by_average_degree,
    read_clusters,
)

DOC_GRAPH_DIR = Path("data/doc_graphs")
DOC_DETAILS_DIR = Path("data/doc_details")
TAXONOMY_DIR = Path("data/taxonomies")
FILEKEYS_PATH = Path("data/filekeys")
CLUSTER_COUNT = 4


def format_filekeys_line(
    graph_name: str, clusters: Sequence[Sequence[ClusterEntry]], order: Sequence[int]
) -> str:
    """Format the ``data/filekeys`` line: name, then one ``<<``-prefixed cluster each.

    The final character of the accumulated string is dropped (intended to remove
    the trailing comma), so an empty last cluster loses one ``<`` instead.
    """
    text = ""
    for cluster_index in order:
        text += "<<"
        for entry in clusters[cluster_index]:
            text += entry.label + ","
        text = text[:-1]
    return graph_name + text


def main(
    doc_graph_dir: Path = DOC_GRAPH_DIR,
    doc_details_dir: Path = DOC_DETAILS_DIR,
    taxonomy_dir: Path = TAXONOMY_DIR,
    filekeys_path: Path = FILEKEYS_PATH,
) -> None:
    filekeys_path.parent.mkdir(parents=True, exist_ok=True)
    with filekeys_path.open("w", encoding="utf-8") as filekeys:
        for graph_path in sorted(doc_graph_dir.iterdir()):
            print(graph_path.name)
            hierarchy = read_gdf(graph_path)
            clusters = read_clusters(
                doc_details_dir / f"{graph_path.stem}.xlsx",
                CLUSTER_COUNT,
                all_sheets=False,
                with_degree=True,
            )
            order = order_clusters_by_average_degree(clusters)
            filekeys.write(format_filekeys_line(graph_path.name, clusters, order) + "\n")

            builder = TaxonomyBuilder(hierarchy)
            builder.add_clusters(clusters, order)
            builder.write_gdf(taxonomy_dir / f"tax{graph_path.name}")


if __name__ == "__main__":
    main()

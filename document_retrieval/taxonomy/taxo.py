"""CLI: assign each concept the nearest concept of the previous cluster as its parent.

Reads cluster membership from a workbook and the hierarchy graph, then writes
the resulting parent links as ``taxonomy2.gdf``.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Mapping, Sequence

from core.gdf_io import format_edge_line, read_gdf
from taxonomy.taxonomy import read_sheet_rows

HIERARCHY_PATH = Path("data/db/introhier.gdf")
WORKBOOK_PATH = Path("data_st.xlsx")
OUTPUT_PATH = Path("taxonomy2.gdf")
CLUSTER_COUNT = 4
CLUSTER_ORDER = [0, 1, 3, 2]


def read_cluster_labels(workbook_path: Path, cluster_count: int) -> list[list[str]]:
    """Return the concept labels of each cluster (apostrophes removed)."""
    clusters: list[list[str]] = [[] for _ in range(cluster_count)]
    for rows in read_sheet_rows(workbook_path, all_sheets=True):
        cluster_column = len(rows[0]) - 1
        for row in rows:
            cluster_number = int(str(row[cluster_column]).replace("cluster", ""))
            clusters[cluster_number].append(str(row[2]).replace("'", ""))
    return clusters


def assign_parents(
    weights: Mapping[str, Mapping[str, float]],
    clusters: Sequence[Sequence[str]],
    order: Sequence[int],
) -> dict[str, str]:
    """Pick, for each concept, the lowest-weight edge from the cluster directly above."""
    parent: dict[str, str] = {}
    for level in range(len(order) - 1):
        for upper in clusters[order[level]]:
            for lower in clusters[order[level + 1]]:
                weight = weights[upper][lower]
                if weight == math.inf:
                    continue
                if lower in parent:
                    if weight < weights[parent[lower]][lower]:
                        parent[lower] = upper
                else:
                    parent[lower] = upper
    return parent


def main(
    hierarchy_path: Path = HIERARCHY_PATH,
    workbook_path: Path = WORKBOOK_PATH,
    output_path: Path = OUTPUT_PATH,
) -> None:
    graph = read_gdf(hierarchy_path)
    labels = [graph.labels[node_id] for node_id in graph.node_ids]
    weights = {row: {col: math.inf for col in labels} for row in labels}
    for edge in graph.edges:
        weights[labels[int(edge.source[1:])]][labels[int(edge.target[1:])]] = edge.weight

    clusters = read_cluster_labels(workbook_path, CLUSTER_COUNT)
    parent = assign_parents(weights, clusters, CLUSTER_ORDER)

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(graph.node_section) + "\n")
        handle.write("edgedef>node1,node2,directed,weight,labelvisible\n")
        for index, label in enumerate(labels):
            if label in parent:
                handle.write(
                    format_edge_line(
                        f"v{index}",
                        f"v{labels.index(parent[label])}",
                        weights[label][parent[label]],
                    )
                    + "\n"
                )


if __name__ == "__main__":
    main()

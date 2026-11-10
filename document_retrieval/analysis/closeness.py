"""CLI: rank hierarchy nodes by closeness centrality (BFS level distances)."""

from __future__ import annotations

import operator
from pathlib import Path

from analysis.bfs_core import bfs_levels
from core.gdf_io import read_gdf

INPUT_PATH = Path("data/db/introhier1.gdf")
OUTPUT_PATH = Path("closeness.txt")


def closeness_of(levels: list[list[int]], node_count: int) -> float:
    """Closeness of the BFS root: ``(n - 1)`` over the sum of node distances."""
    distance_sum = sum(depth * len(level) for depth, level in enumerate(levels))
    if distance_sum == 0:
        return 0.0
    return (node_count - 1) / distance_sum


def main(input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_PATH) -> None:
    graph = read_gdf(input_path)
    adjacency = graph.adjacency_lists()
    labels = [graph.labels[node_id] for node_id in graph.node_ids]

    closeness = {
        labels[root]: closeness_of(bfs_levels(adjacency, root).levels, graph.node_count)
        for root in range(graph.node_count)
    }
    ranked = sorted(closeness.items(), key=operator.itemgetter(1), reverse=True)

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("\nlinedef>node,label,closeness\n")
        for label, value in ranked:
            handle.write(f"v{labels.index(label)},{label},{value}\n")


if __name__ == "__main__":
    main()

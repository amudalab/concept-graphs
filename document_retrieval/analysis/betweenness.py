"""CLI: rank nodes of the combined shortest-path-tree graph by betweenness."""

from __future__ import annotations

import operator
from pathlib import Path

from core.gdf_io import read_gdf

INPUT_PATH = Path("shortest_path_tree1/comp_shortest_path_tree.gdf")
OUTPUT_PATH = Path("betweenness1.txt")


def main(input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_PATH) -> None:
    graph = read_gdf(input_path)
    weights = graph.weight_matrix(0)
    size = graph.node_count

    betweenness = {}
    for i, node_id in enumerate(graph.node_ids):
        total = sum(weights[i])
        betweenness[node_id] = (
            ((total - (2 * (size - 1))) / 2) + (2 * (size - 1))
        ) / (size * size)
    ranked = sorted(betweenness.items(), key=operator.itemgetter(1), reverse=True)
    max_value = ranked[0][1]

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("linedef>node,label,betweenness\n")
        for node_id, value in ranked:
            handle.write(f"{node_id},{graph.labels[node_id]},{value / max_value}\n")


if __name__ == "__main__":
    main()

"""CLI: rank hierarchy nodes by strength (sum of outgoing edge weights)."""

from __future__ import annotations

import operator
from pathlib import Path

from core.gdf_io import read_gdf

INPUT_PATH = Path("data/db/introhier.gdf")
OUTPUT_PATH = Path("data/strength.txt")


def main(input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_PATH) -> None:
    graph = read_gdf(input_path)
    weights = graph.weight_matrix(0)

    strength = {
        node_id: sum(weights[i]) for i, node_id in enumerate(graph.node_ids)
    }
    ranked = sorted(strength.items(), key=operator.itemgetter(1), reverse=True)

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("linedef>node,label,strength\n")
        for node_id, value in ranked:
            handle.write(f"{node_id},{graph.labels[node_id]},{value}\n")


if __name__ == "__main__":
    main()

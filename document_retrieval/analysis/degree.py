"""CLI: rank hierarchy nodes by (normalised) out-degree."""

from __future__ import annotations

import math
import operator
from pathlib import Path

from core.gdf_io import read_gdf

INPUT_PATH = Path("data/db/introhier2.gdf")
OUTPUT_PATH = Path("degree2.txt")


def main(input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_PATH) -> None:
    graph = read_gdf(input_path)
    weights = graph.weight_matrix(math.inf)

    degree = {
        node_id: float(sum(1 for weight in weights[i] if weight != math.inf))
        for i, node_id in enumerate(graph.node_ids)
    }
    ranked = sorted(degree.items(), key=operator.itemgetter(1), reverse=True)
    max_degree = ranked[0][1]

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("linedef>node,label,degree\n")
        for node_id, value in ranked:
            handle.write(f"{node_id},{graph.labels[node_id]},{value / max_degree}\n")


if __name__ == "__main__":
    main()

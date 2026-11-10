"""CLI: split the hierarchy graph into low/high-weight subgraphs at 100%..0% of the max weight."""

from __future__ import annotations

import math
from pathlib import Path

from core.gdf_io import format_edge_line, read_gdf, write_gdf

INPUT_PATH = Path("data/db/introhier.gdf")
OUTPUT_DIR = Path("data/cluster")
_EDGE_HEADER = "edgedef> node1,node2,directed,weight,labelvisible"


def main(input_path: Path = INPUT_PATH, output_dir: Path = OUTPUT_DIR) -> None:
    graph = read_gdf(input_path)
    weights = graph.weight_matrix(math.inf)
    max_weight = max((edge.weight for edge in graph.edges), default=0)

    percent = 1.0
    while percent > 0.0:
        cut_off = max_weight * percent
        lower_lines: list[str] = []
        upper_lines: list[str] = []
        for i, row in enumerate(weights):
            for j, weight in enumerate(row):
                if weight == math.inf:
                    continue
                line = format_edge_line(f"v{i}", f"v{j}", weight)
                if weight <= cut_off:
                    lower_lines.append(line)
                elif weight >= cut_off:
                    upper_lines.append(line)
        label = int(percent * 100)
        write_gdf(
            output_dir / f"lessthan{label}.gdf",
            graph.node_section,
            lower_lines,
            edge_header=_EDGE_HEADER,
        )
        write_gdf(
            output_dir / f"greaterthan{label}.gdf",
            graph.node_section,
            upper_lines,
            edge_header=_EDGE_HEADER,
        )
        percent -= 0.1


if __name__ == "__main__":
    main()

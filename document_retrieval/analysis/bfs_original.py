"""CLI: write the full BFS tree of the hierarchy graph from a fixed root."""

from __future__ import annotations

from pathlib import Path

from analysis.bfs_core import HIERARCHY_GDF, bfs_levels, load_hierarchy
from core.gdf_io import format_edge_line, write_gdf

ROOT_NODE = 43
OUTPUT_PATH = Path("data/bfs.gdf")


def main(
    input_path: Path = HIERARCHY_GDF,
    output_path: Path = OUTPUT_PATH,
    root: int = ROOT_NODE,
) -> None:
    graph, weights, adjacency = load_hierarchy(input_path)
    result = bfs_levels(adjacency, root)
    edge_lines = [
        format_edge_line(f"v{parent}", f"v{child}", weights[parent][child])
        for parent, child in result.tree_edges
    ]
    write_gdf(
        output_path,
        graph.node_section,
        edge_lines,
        blank_line_before_edges=True,
    )
    print(f"{len(result.levels)} BFS levels from v{root}; wrote {output_path}")


if __name__ == "__main__":
    main()

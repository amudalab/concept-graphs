"""CLI: BFS from a root, writing the full tree and the first K levels separately."""

from __future__ import annotations

from pathlib import Path

from analysis.bfs_core import HIERARCHY_GDF, bfs_levels, load_hierarchy
from core.gdf_io import format_edge_line, write_gdf

ROOT_NODE = 112
LEVEL_COUNT = 3
TREE_OUTPUT_PATH = Path("data/bfs_from_root.gdf")
LEVELS_OUTPUT_PATH = Path("data/bfs_K_levels_from_rank.gdf")


def main(
    input_path: Path = HIERARCHY_GDF,
    root: int = ROOT_NODE,
    level_count: int = LEVEL_COUNT,
) -> None:
    graph, weights, adjacency = load_hierarchy(input_path)
    result = bfs_levels(adjacency, root)

    tree_edge_lines = [
        format_edge_line(f"v{parent}", f"v{child}", weights[parent][child])
        for parent, child in result.tree_edges
    ]

    # Edges between consecutive levels; each node of the next level is
    # attached once, through the first node of the current level that reaches it.
    levels = result.levels
    level_edge_lines = []
    for depth in range(min(level_count - 1, len(levels) - 1)):
        attached: set[int] = set()
        next_level = set(levels[depth + 1])
        for node in levels[depth]:
            for child in adjacency[node]:
                if child in next_level and child not in attached:
                    level_edge_lines.append(
                        format_edge_line(f"v{node}", f"v{child}", weights[node][child])
                    )
                    attached.add(child)

    write_gdf(TREE_OUTPUT_PATH, graph.node_section, tree_edge_lines, blank_line_before_edges=True)
    write_gdf(LEVELS_OUTPUT_PATH, graph.node_section, level_edge_lines, blank_line_before_edges=True)
    print(f"{len(levels)} BFS levels from v{root}")


if __name__ == "__main__":
    main()

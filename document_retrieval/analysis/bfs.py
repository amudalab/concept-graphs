"""Breadth-first search over a weighted term graph (used for query/document graphs)."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

from analysis.bfs_core import bfs_levels

QUERY_BFS_PATH = Path("data/querybfs.gdf")


def run_bfs(
    graph: Mapping[str, Sequence[str]],
    weight_graph: Mapping[str, Mapping[str, float]],
    root: str,
    *,
    output_path: Path | None = QUERY_BFS_PATH,
) -> tuple[dict[str, dict[str, float]], int]:
    """Run BFS from ``root`` and return ``(tree_weights, level_count)``.

    ``tree_weights[a][b]`` holds the edge weight for every BFS-tree edge (in
    both directions) and ``0`` elsewhere.  The tree edges are also written to
    ``output_path`` (pass ``None`` to skip writing).
    """
    result = bfs_levels(graph, root)

    tree_weights: dict[str, dict[str, float]] = {
        source: {target: 0 for target in graph} for source in graph
    }
    edge_lines = []
    for parent, child in result.tree_edges:
        weight = weight_graph[parent][child]
        tree_weights[parent][child] = weight
        tree_weights[child][parent] = weight
        edge_lines.append(f"{parent},{child},false,{weight},true\n")

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as handle:
            handle.writelines(edge_lines)

    return tree_weights, len(result.levels)

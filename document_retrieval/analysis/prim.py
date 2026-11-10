"""Prim's minimum spanning tree over a GDF weight matrix.

Adapted from Tim Wilson's list-based implementation (2-25-2002).
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from core.gdf_io import format_edge_line, node_number, read_gdf, write_gdf

INPUT_PATH = Path("output/comp_introhier.gdf")
OUTPUT_PATH = Path("data/minimum_spanning.gdf")
ROOT_NODE = 17

# Stand-in for "infinity" in the key array.
_LARGE_KEY = 999999


def minimum_spanning_tree(
    vertices: Sequence[int], matrix: Sequence[Sequence[float]], root: int
) -> list[int | None]:
    """Return the Prim parent of every vertex (``None`` for the root / unreachable ones).

    ``matrix[u][v] > 0`` denotes an edge; ``vertices`` are the row/column indices.
    """
    parent: list[int | None] = [None] * len(vertices)
    key: list[float] = [_LARGE_KEY] * len(vertices)
    queue = list(vertices)

    key[root] = 0
    _sort_queue_by_key(queue, key)

    while queue:
        u = queue.pop(0)
        for v in _adjacent_vertices(matrix, u):
            weight = matrix[u][v]
            if v in queue and weight < key[v]:
                parent[v] = u
                key[v] = weight
                _sort_queue_by_key(queue, key)
    return parent


def _adjacent_vertices(matrix: Sequence[Sequence[float]], u: int) -> list[int]:
    """Neighbours of ``u`` in descending vertex order."""
    neighbors: list[int] = []
    for x in range(len(matrix)):
        if matrix[u][x] > 0 and x != u:
            neighbors.insert(0, x)
    return neighbors


def _sort_queue_by_key(queue: list[int], key: Sequence[float]) -> None:
    """Order ``queue`` by ascending key (exchange sort, as in the original)."""
    for i in range(len(queue)):
        for j in range(len(queue)):
            if key[queue[i]] < key[queue[j]]:
                queue[i], queue[j] = queue[j], queue[i]


def main(
    input_path: Path = INPUT_PATH,
    output_path: Path = OUTPUT_PATH,
    root: int = ROOT_NODE,
) -> None:
    graph = read_gdf(input_path)
    matrix = graph.weight_matrix(0)
    vertices = [node_number(node_id) for node_id in graph.node_ids]
    parent = minimum_spanning_tree(vertices, matrix, root)

    node_section = ["nodedef> name,label"] + [
        line
        for i, line in enumerate(graph.node_lines())
        if i < len(parent) and (parent[i] is not None or i == root)
    ]
    edge_lines = [
        format_edge_line(f"v{i}", f"v{p}", matrix[i][p])
        for i, p in enumerate(parent)
        if p is not None
    ]
    write_gdf(output_path, node_section, edge_lines, blank_line_before_edges=True)


if __name__ == "__main__":
    main()

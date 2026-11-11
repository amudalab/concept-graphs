"""Scale hierarchy edge weights by taxonomy path length (enhanced semantic net).

Every edge ``u -> v`` of the hierarchy graph is multiplied by the length of
the shortest path from ``u`` to ``v`` in the taxonomy graph, divided by
:data:`PATH_LENGTH_NORMALIZER`.
"""

from __future__ import annotations

import math
from collections import deque
from pathlib import Path
from typing import Mapping, Sequence

from core.gdf_io import GdfGraph, matrix_edge_lines, node_number, read_gdf, write_gdf

TAXONOMY_PATH = Path("data/taxEM.gdf")
HIERARCHY_PATH = Path("data/db/introhier.gdf")
OUTPUT_PATH = Path("data/enhanced_semantic_net.gdf")
PATH_LENGTH_NORMALIZER = 6


def shortest_path_length(
    graph: Mapping[str, Sequence[str]], start: str, end: str
) -> int | None:
    """Return the fewest edges on any simple path ``start -> end``, or ``None``.

    Like the original implementation, this explores every simple path
    breadth-first, so it is only suitable for small, sparse taxonomies.
    """
    best: int | None = None
    queue: deque[list[str]] = deque([[start]])
    while queue:
        path = queue.popleft()
        last_node = path[-1]
        if last_node == end:
            length = len(path) - 1
            if best is None or length < best:
                best = length
        for neighbor in graph[last_node]:
            if neighbor not in path:
                queue.append(path + [neighbor])
    return best


def enhance_weights(taxonomy: GdfGraph, hierarchy: GdfGraph) -> list[list[float]]:
    """Return the hierarchy weights scaled by taxonomy distance.

    The matrix is sized by the taxonomy's node count.  Absent edges are
    ``math.inf``; edges whose endpoints are not connected in the taxonomy keep
    their original weight.
    """
    size = taxonomy.node_count
    matrix = [[math.inf] * size for _ in range(size)]
    for edge in hierarchy.edges:
        matrix[node_number(edge.source)][node_number(edge.target)] = edge.weight

    taxonomy_adjacency = taxonomy.adjacency_by_id()
    for row in range(size):
        for col in range(size):
            if matrix[row][col] == math.inf:
                continue
            length = shortest_path_length(taxonomy_adjacency, f"v{row}", f"v{col}")
            if length is not None:
                matrix[row][col] = (matrix[row][col] * length) / PATH_LENGTH_NORMALIZER
    return matrix


def enhance_file(taxonomy_path: Path, hierarchy_path: Path, output_path: Path) -> None:
    """Read a taxonomy and hierarchy GDF and write the enhanced net."""
    taxonomy = read_gdf(taxonomy_path)
    hierarchy = read_gdf(hierarchy_path)
    matrix = enhance_weights(taxonomy, hierarchy)
    write_gdf(output_path, hierarchy.node_section, matrix_edge_lines(matrix))


def main() -> None:
    enhance_file(TAXONOMY_PATH, HIERARCHY_PATH, OUTPUT_PATH)


if __name__ == "__main__":
    main()

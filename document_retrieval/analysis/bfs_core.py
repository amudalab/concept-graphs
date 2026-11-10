"""Shared breadth-first-search helpers (internal to ``document_retrieval``)."""

from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Hashable, Mapping, NamedTuple, Sequence, TypeVar

from core.gdf_io import GdfGraph, read_gdf

Node = TypeVar("Node", bound=Hashable)

HIERARCHY_GDF = Path("data/db/introhier.gdf")


class BfsResult(NamedTuple):
    """Outcome of :func:`bfs_levels`."""

    levels: list[list]
    """Nodes grouped by distance from the root (``levels[0] == [root]``)."""

    tree_edges: list[tuple]
    """``(parent, child)`` pairs in the order the BFS discovered them."""


def bfs_levels(
    adjacency: Mapping[Node, Sequence[Node]] | Sequence[Sequence[Node]], root: Node
) -> BfsResult:
    """Run a breadth-first search from ``root``.

    ``adjacency`` maps each node (dict key or list index) to its neighbours.
    """
    seen = {root}
    queue = deque([root])
    depth = {root: 0}
    levels: list[list[Node]] = [[root]]
    tree_edges: list[tuple[Node, Node]] = []
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current]:  # type: ignore[call-overload,index]
            if neighbor in seen:
                continue
            seen.add(neighbor)
            queue.append(neighbor)
            tree_edges.append((current, neighbor))
            depth[neighbor] = depth[current] + 1
            if depth[neighbor] == len(levels):
                levels.append([])
            levels[depth[neighbor]].append(neighbor)
    return BfsResult(levels, tree_edges)


def load_hierarchy(path: Path = HIERARCHY_GDF) -> tuple[GdfGraph, list[list[float]], list[list[int]]]:
    """Read a hierarchy GDF and return ``(graph, weight_matrix, adjacency_lists)``."""
    graph = read_gdf(path)
    return graph, graph.weight_matrix(0), graph.adjacency_lists()

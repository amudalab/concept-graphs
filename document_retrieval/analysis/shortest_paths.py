"""Undirected weighted graph with Dijkstra shortest paths.

Shared by the taxonomy builders and the shortest-path-tree scripts.
"""

from __future__ import annotations

import heapq
import sys
from pathlib import Path
from typing import Iterable

from core.gdf_io import GdfGraph, format_edge_line, node_number, read_gdf, write_gdf


class Vertex:
    """A graph vertex carrying Dijkstra bookkeeping."""

    def __init__(self, node_id: str, order: int) -> None:
        self.id = node_id
        self.order = order
        self.adjacent: dict[Vertex, float] = {}
        self.distance: float = sys.maxsize
        self.visited = False
        self.previous: Vertex | None = None

    def add_neighbor(self, neighbor: Vertex, weight: float = 0) -> None:
        self.adjacent[neighbor] = weight

    def reset(self) -> None:
        """Clear Dijkstra state so the vertex can be reused for another run."""
        self.distance = sys.maxsize
        self.visited = False
        self.previous = None

    def __repr__(self) -> str:
        return f"{self.id} adjacent: {[vertex.id for vertex in self.adjacent]}"


class Graph:
    """Undirected weighted graph keyed by node id."""

    def __init__(self) -> None:
        self.vertices: dict[str, Vertex] = {}

    def __iter__(self):
        return iter(self.vertices.values())

    def add_vertex(self, node_id: str) -> Vertex:
        vertex = Vertex(node_id, len(self.vertices))
        self.vertices[node_id] = vertex
        return vertex

    def get_vertex(self, node_id: str) -> Vertex | None:
        return self.vertices.get(node_id)

    def add_edge(self, source: str, target: str, cost: float = 0) -> None:
        if source not in self.vertices:
            self.add_vertex(source)
        if target not in self.vertices:
            self.add_vertex(target)
        self.vertices[source].add_neighbor(self.vertices[target], cost)
        self.vertices[target].add_neighbor(self.vertices[source], cost)

    def reset(self) -> None:
        for vertex in self:
            vertex.reset()


def graph_from_gdf(gdf: GdfGraph) -> Graph:
    """Build an undirected :class:`Graph` from a parsed GDF."""
    graph = Graph()
    for node_id in gdf.node_ids:
        graph.add_vertex(node_id)
    for edge in gdf.edges:
        graph.add_edge(edge.source, edge.target, edge.weight)
    return graph


def dijkstra(graph: Graph, start: Vertex) -> None:
    """Compute shortest distances from ``start``, filling ``distance``/``previous``.

    Ties between equally close vertices are broken by insertion order.  The
    graph's state is reset first, so it can be reused across runs.
    """
    graph.reset()
    start.distance = 0
    queue = [(vertex.distance, vertex.order, vertex) for vertex in graph]
    heapq.heapify(queue)
    while queue:
        distance, _, current = heapq.heappop(queue)
        if current.visited or distance != current.distance:
            continue
        current.visited = True
        for neighbor, weight in current.adjacent.items():
            if neighbor.visited:
                continue
            new_distance = current.distance + weight
            if new_distance < neighbor.distance:
                neighbor.distance = new_distance
                neighbor.previous = current
                heapq.heappush(queue, (new_distance, neighbor.order, neighbor))


def path_to_root(target: Vertex) -> list[str]:
    """Return node ids from ``target`` back to the Dijkstra source.

    A vertex that was never reached yields just ``[target.id]``.
    """
    path = [target.id]
    vertex = target
    while vertex.previous is not None:
        vertex = vertex.previous
        path.append(vertex.id)
    return path


def path_length(path: Iterable[str], weights: dict[tuple[str, str], float]) -> float:
    """Sum the weight of consecutive ``(a, b)`` hops along ``path``."""
    nodes = list(path)
    return sum(weights.get((a, b), 0.0) for a, b in zip(nodes, nodes[1:]))


def _count_matrix(size: int) -> list[list[int]]:
    return [[0] * size for _ in range(size)]


def _count_edge_lines(counts: list[list[int]], reference: list[list[int]]) -> list[str]:
    """Edge lines with ``counts`` as weights, for cells where ``reference`` > 0."""
    return [
        format_edge_line(f"v{i}", f"v{j}", counts[i][j])
        for i in range(len(reference))
        for j in range(len(reference))
        if reference[i][j] > 0
    ]


def _accumulate_tree_edges(
    graph: Graph, node_ids: list[str], *counters: list[list[int]]
) -> None:
    """Add every shortest-path hop to the (symmetric) ``counters``."""
    for target_id in node_ids:
        path = path_to_root(graph.vertices[target_id])
        for here, there in zip(path, path[1:]):
            a, b = node_number(here), node_number(there)
            for counter in counters:
                counter[a][b] += 1
                counter[b][a] += 1


def write_all_pairs_shortest_path_trees(input_path: Path, output_dir: Path) -> None:
    """Write one shortest-path tree per source node plus a combined graph.

    Per-source files are ``comp_shortest_path_tree_from_<label>.gdf`` with hop
    counts as weights.  ``comp_shortest_path_tree.gdf`` carries the hop counts
    accumulated over all sources, but (as in the original script) only for the
    edges used by the *last* source's tree.
    """
    gdf = read_gdf(input_path)
    graph = graph_from_gdf(gdf)
    size = gdf.node_count
    combined = _count_matrix(size)
    last_tree = _count_matrix(size)
    for source_id in gdf.node_ids:
        dijkstra(graph, graph.vertices[source_id])
        last_tree = _count_matrix(size)
        _accumulate_tree_edges(graph, gdf.node_ids, last_tree, combined)
        write_gdf(
            output_dir / f"comp_shortest_path_tree_from_{gdf.labels[source_id]}.gdf",
            gdf.node_section,
            _count_edge_lines(last_tree, last_tree),
            blank_line_before_edges=True,
        )
    write_gdf(
        output_dir / "comp_shortest_path_tree.gdf",
        gdf.node_section,
        _count_edge_lines(combined, last_tree),
        blank_line_before_edges=True,
    )


def write_single_source_shortest_path_tree(
    input_path: Path, source_id: str, output_path: Path
) -> None:
    """Write the shortest-path tree rooted at ``source_id`` (hop counts as weights)."""
    gdf = read_gdf(input_path)
    graph = graph_from_gdf(gdf)
    dijkstra(graph, graph.vertices[source_id])
    counts = _count_matrix(gdf.node_count)
    _accumulate_tree_edges(graph, gdf.node_ids, counts)
    write_gdf(
        output_path,
        gdf.node_section,
        _count_edge_lines(counts, counts),
        blank_line_before_edges=True,
    )

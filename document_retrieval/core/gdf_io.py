"""Read and write the GDF graph files used throughout this package.

A GDF file has a ``nodedef>`` section (``vN,label`` lines) followed by an
``edgedef>`` section (``vA,vB,directed,weight,labelvisible`` lines).  The
parsing rules here mirror the original ad-hoc scripts: a line with exactly two
comma-separated fields is a node line, a line with exactly five fields is an
edge line, and the first line of each kind is the section header.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

NODE_HEADER = "nodedef> name,label"
EDGE_HEADER = "edgedef>node1,node2,directed,weight,labelvisible"


@dataclass(frozen=True)
class GdfEdge:
    """One edge line of a GDF file."""

    source: str
    target: str
    weight: float


@dataclass
class GdfGraph:
    """Parsed contents of a GDF file."""

    node_section: list[str] = field(default_factory=list)
    node_ids: list[str] = field(default_factory=list)
    labels: dict[str, str] = field(default_factory=dict)
    edges: list[GdfEdge] = field(default_factory=list)

    @property
    def node_count(self) -> int:
        """Number of nodes (header excluded)."""
        return len(self.node_ids)

    def node_lines(self) -> list[str]:
        """Return only the ``vN,label`` lines (header excluded)."""
        return self.node_section[1:]

    def weight_matrix(self, fill: float = 0.0) -> list[list[float]]:
        """Return a dense ``node_count`` x ``node_count`` weight matrix.

        Cells for absent edges hold ``fill``; edges are addressed by the
        numeric part of their ``vN`` identifiers.
        """
        size = self.node_count
        matrix = [[fill] * size for _ in range(size)]
        for edge in self.edges:
            matrix[node_number(edge.source)][node_number(edge.target)] = edge.weight
        return matrix

    def adjacency_lists(self) -> list[list[int]]:
        """Return out-neighbour lists indexed by node number."""
        adjacency: list[list[int]] = [[] for _ in range(self.node_count)]
        for edge in self.edges:
            adjacency[node_number(edge.source)].append(node_number(edge.target))
        return adjacency

    def adjacency_by_id(self) -> dict[str, list[str]]:
        """Return out-neighbour lists keyed by node identifier."""
        adjacency: dict[str, list[str]] = {node_id: [] for node_id in self.node_ids}
        for edge in self.edges:
            adjacency[edge.source].append(edge.target)
        return adjacency


def node_number(node_id: str) -> int:
    """Return the integer part of a ``vN`` node identifier."""
    return int(node_id[1:])


def parse_gdf_lines(lines: Iterable[str]) -> GdfGraph:
    """Parse already-split GDF lines into a :class:`GdfGraph`."""
    graph = GdfGraph()
    seen_node_header = False
    seen_edge_header = False
    for raw_line in lines:
        line = raw_line.rstrip("\r")
        fields = line.split(",")
        if len(fields) == 2:
            graph.node_section.append(line)
            if seen_node_header:
                graph.node_ids.append(fields[0])
                graph.labels[fields[0]] = fields[1]
            seen_node_header = True
        elif len(fields) == 5:
            if seen_edge_header:
                graph.edges.append(GdfEdge(fields[0], fields[1], float(fields[3])))
            seen_edge_header = True
    return graph


def read_gdf(path: str | Path) -> GdfGraph:
    """Read and parse a GDF file."""
    text = Path(path).read_text(encoding="utf-8")
    return parse_gdf_lines(text.split("\n"))


def format_edge_line(source: str, target: str, weight: object) -> str:
    """Format an undirected, label-visible edge line."""
    return f"{source},{target},false,{weight},true"


def matrix_edge_lines(
    matrix: Sequence[Sequence[float]], absent: float = math.inf
) -> list[str]:
    """Return edge lines for every cell of ``matrix`` that differs from ``absent``."""
    lines = []
    for i, row in enumerate(matrix):
        for j, weight in enumerate(row):
            if weight != absent:
                lines.append(format_edge_line(f"v{i}", f"v{j}", weight))
    return lines


def write_gdf(
    path: str | Path,
    node_section: Sequence[str],
    edge_lines: Iterable[str],
    *,
    blank_line_before_edges: bool = False,
    edge_header: str = EDGE_HEADER,
) -> None:
    """Write a GDF file.

    ``node_section`` must include the ``nodedef>`` header line followed by the
    node lines (see :attr:`GdfGraph.node_section`).
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for line in node_section:
            handle.write(line + "\n")
        if blank_line_before_edges:
            handle.write("\n")
        handle.write(edge_header + "\n")
        for line in edge_lines:
            handle.write(line + "\n")

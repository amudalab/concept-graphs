#!/usr/bin/env python3
"""Extract an energy-bounded BFS subgraph from a Guise .gdf graph."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Set, Tuple


def load_gdf(path: Path) -> Tuple[List[int], List[List[float]]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    nodes: List[int] = []
    seeing_nodes = False
    for line in lines:
        parts = line.split(",")
        if len(parts) == 2:
            if seeing_nodes:
                nodes.append(int(parts[0][1:]))
            seeing_nodes = True
        elif seeing_nodes:
            break

    size = len(nodes)
    weights = [[0.0 for _ in range(size)] for _ in range(size)]
    seeing_edges = False
    for line in lines:
        parts = line.split(",")
        if len(parts) == 5:
            if seeing_edges:
                source = int(parts[0][1:])
                target = int(parts[1][1:])
                weights[source][target] = float(parts[3])
            seeing_edges = True
    return nodes, weights


def adjacency_lists(weights: Sequence[Sequence[float]]) -> Dict[int, List[int]]:
    return {
        source: [target for target, weight in enumerate(row) if weight]
        for source, row in enumerate(weights)
    }


def energy_bfs(
    graph: Mapping[int, Sequence[int]],
    weights: Sequence[Sequence[float]],
    *,
    root: int,
    initial_energy: float = 14600.0,
    threshold: float = 10.0,
) -> List[Tuple[int, int, float]]:
    """Return directed edges discovered by the energy-bounded BFS."""
    max_weight = max((max(row) for row in weights), default=1.0) or 1.0
    pending: List[int] = [root]
    energies: List[float] = [initial_energy]
    visited: Set[int] = set()
    edges: List[Tuple[int, int, float]] = []

    while pending:
        node = pending.pop(0)
        energy = energies.pop(0)
        if node in visited:
            continue
        visited.add(node)
        neighbours = list(graph.get(node, ()))
        if not neighbours:
            continue
        if energy / float(len(neighbours)) < threshold:
            continue
        for neighbour in neighbours:
            weight = weights[node][neighbour]
            edges.append((node, neighbour, weight))
            if neighbour not in visited and neighbour not in pending:
                pending.append(neighbour)
                energies.append(energy * weight / (len(neighbours) * max_weight))
    return edges


def write_subgraph(
    edges: Sequence[Tuple[int, int, float]],
    destination: Path,
) -> None:
    lines = ["nodedef>name VARCHAR,label VARCHAR"]
    used = sorted({node for edge in edges for node in edge[:2]})
    for node in used:
        lines.append(f"v{node},{node}")
    lines.append(
        "edgedef>node1 VARCHAR,node2 VARCHAR,directed BOOLEAN,weight DOUBLE,label BOOLEAN"
    )
    for source, target, weight in edges:
        lines.append(f"v{source},v{target},false,{weight},true")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, default=Path("data/dsfull1.gdf"))
    parser.add_argument("--root", type=int, default=0)
    parser.add_argument("--output", type=Path, default=Path("data/subgraph.gdf"))
    args = parser.parse_args(argv)

    _nodes, weights = load_gdf(args.graph)
    graph = adjacency_lists(weights)
    edges = energy_bfs(graph, weights, root=args.root)
    write_subgraph(edges, args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Biconnected components and articulation points of an undirected graph.

A Hopcroft-Tarjan non-recursive depth-first search that tracks the highest
level reached by back edges.  Adapted from NetworkX 1.x.

Copyright (C) 2011 by Aric Hagberg, Dan Schult and Pieter Swart.
Original authors: Jordi Torrents, Dan Schult, Aric Hagberg.  BSD license.

Reference: Hopcroft, J.; Tarjan, R. (1973). "Efficient algorithms for graph
manipulation". Communications of the ACM 16: 372-378.
"""

from __future__ import annotations

from itertools import chain
from typing import Hashable, Iterator

import networkx as nx

__all__ = [
    "articulation_points",
    "biconnected_component_edges",
    "biconnected_components",
    "is_biconnected",
]

Edge = tuple[Hashable, Hashable]


def is_biconnected(graph: nx.Graph) -> bool:
    """Return True if ``graph`` cannot be disconnected by removing one node."""
    components = biconnected_components(graph)
    if not components:  # an empty graph has no bicomponents
        return False
    return len(components[0]) == len(graph)


def biconnected_component_edges(graph: nx.Graph) -> list[list[Edge]]:
    """Return the edge list of each biconnected component, largest first."""
    return sorted(_biconnected_dfs(graph, components=True), key=len, reverse=True)


def biconnected_components(graph: nx.Graph) -> list[set[Hashable]]:
    """Return the node set of each biconnected component, largest first."""
    components = (
        set(chain.from_iterable(edges))
        for edges in _biconnected_dfs(graph, components=True)
    )
    return sorted(components, key=len, reverse=True)


def articulation_points(graph: nx.Graph) -> Iterator[Hashable]:
    """Yield the articulation points (cut vertices) of ``graph``."""
    return _biconnected_dfs(graph, components=False)


def _biconnected_dfs(graph: nx.Graph, components: bool = True) -> Iterator:
    """Yield biconnected components (as edge lists) or articulation points."""
    if graph.is_directed():
        raise nx.NetworkXError(
            "Not allowed for directed graph G. "
            "Use UG=G.to_undirected() to create an undirected graph."
        )
    visited: set[Hashable] = set()
    for start in graph:
        if start in visited:
            continue
        discovery = {start: 0}  # "time" of first discovery of each node
        low = {start: 0}
        root_children = 0
        visited.add(start)
        edge_stack: list[Edge] = []
        stack = [(start, start, iter(graph[start]))]
        while stack:
            grandparent, parent, children = stack[-1]
            try:
                child = next(children)
                if grandparent == child:
                    continue
                if child in visited:
                    if discovery[child] <= discovery[parent]:  # back edge
                        low[parent] = min(low[parent], discovery[child])
                        if components:
                            edge_stack.append((parent, child))
                else:
                    low[child] = discovery[child] = len(discovery)
                    visited.add(child)
                    stack.append((parent, child, iter(graph[child])))
                    if components:
                        edge_stack.append((parent, child))
            except StopIteration:
                stack.pop()
                if len(stack) > 1:
                    if low[parent] >= discovery[grandparent]:
                        if components:
                            index = edge_stack.index((grandparent, parent))
                            yield edge_stack[index:]
                            edge_stack = edge_stack[:index]
                        else:
                            yield grandparent
                    low[grandparent] = min(low[parent], low[grandparent])
                elif stack:  # length 1, so grandparent is the root
                    root_children += 1
                    if components:
                        index = edge_stack.index((grandparent, parent))
                        yield edge_stack[index:]
        if not components and root_children > 1:
            # The root is an articulation point if it has more than one child.
            yield start

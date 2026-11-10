"""Document retrieval over edge-enhanced semantic nets.

The query graph and each candidate document's enhanced semantic net are
BFS-expanded from the query's highest-degree terms; documents are ranked by
the distance between the two BFS trees.
"""

from __future__ import annotations

import math
import operator
import sys
from pathlib import Path

import core.graph_init as graph_init
from retrieval.common import build_query_graph, load_document_keys
from analysis.bfs import run_bfs
from core.gdf_io import read_gdf

ENHANCED_NET_DIR = Path("data/enhanced_semantic_nets")
MAX_RESULT_COUNT = 11


def retrieve_documents(query: str) -> list[str]:
    """Return document names ordered by BFS-tree distance to the query graph."""
    query_terms = build_query_graph(query)
    matrix = graph_init.get_matrix()
    cells = matrix.gmatrix
    max_updates = matrix.get_max_update_count(query_terms)

    degree: dict[str, float] = {}
    adjacency: dict[str, list[str]] = {}
    weights: dict[str, dict[str, float]] = {}
    for term in query_terms:
        degree[term] = 0.0
        adjacency[term] = []
        weights[term] = {}
        for other in query_terms:
            if cells[term][other].weight != float("inf"):
                adjacency[term].append(other)
                weights[term][other] = cells[term][other].normalized_weight(max_updates)
                degree[term] += 1
            else:
                weights[term][other] = 0
    terms_by_degree = sorted(degree.items(), key=operator.itemgetter(1))[::-1]

    documents = load_document_keys()
    net_cache: dict[str, tuple[dict[str, list[str]], dict[str, dict[str, float]]]] = {}
    distance_by_document: dict[str, float] = {}

    rank = 0
    while len(distance_by_document) < MAX_RESULT_COUNT and rank < len(terms_by_degree):
        root_term = terms_by_degree[rank][0]
        query_tree, _ = run_bfs(adjacency, weights, root_term)
        for name, document in documents.items():
            if root_term not in document.keys:
                continue
            if name not in net_cache:
                net_cache[name] = _load_enhanced_net(name)
            document_adjacency, document_weights = net_cache[name]
            document_tree, _ = run_bfs(document_adjacency, document_weights, root_term)

            shared_terms = set(query_terms) & set(document.keys)
            squared_distance = 0.0
            for row_term in query_terms:
                for col_term in query_terms:
                    if row_term in shared_terms and col_term in shared_terms:
                        squared_distance += (
                            query_tree[row_term][col_term]
                            - document_tree[row_term][col_term]
                        ) ** 2
                    else:
                        squared_distance += query_tree[row_term][col_term] ** 2
            distance = math.sqrt(squared_distance)
            if name not in distance_by_document or distance < distance_by_document[name]:
                distance_by_document[name] = distance
        rank += 1

    ranked = sorted(distance_by_document.items(), key=operator.itemgetter(1))
    return [name for name, _ in ranked]


def _load_enhanced_net(
    document_name: str,
) -> tuple[dict[str, list[str]], dict[str, dict[str, float]]]:
    """Load a document's enhanced net as label-keyed adjacency and weight maps."""
    net = read_gdf(ENHANCED_NET_DIR / f"enhanced_semantic_net_{document_name}")
    adjacency: dict[str, list[str]] = {}
    weights: dict[str, dict[str, float]] = {}
    for node_id in net.node_ids:
        adjacency[net.labels[node_id]] = []
        weights[net.labels[node_id]] = {}
    for edge in net.edges:
        source = net.labels[edge.source]
        target = net.labels[edge.target]
        adjacency[source].append(target)
        weights[source][target] = edge.weight
    return adjacency, weights


def main(argv: list[str] | None = None) -> None:
    arguments = sys.argv[1:] if argv is None else argv
    for name in retrieve_documents(" ".join(arguments)):
        print(name)


if __name__ == "__main__":
    main()

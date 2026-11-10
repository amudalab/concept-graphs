"""CLI: list node triples ``i -> j`` with a shared intermediate ``k`` in the hierarchy graph."""

from __future__ import annotations

from pathlib import Path

from core.gdf_io import read_gdf

INPUT_PATH = Path("data/db/introhier.gdf")


def find_triangles(weights: list[list[float]]) -> list[tuple[int, int, int]]:
    """Return ``(i, j, k)`` where ``i->j``, ``i->k`` and ``k->j`` all exist."""
    size = len(weights)
    triangles = []
    for i in range(size):
        for j in range(size):
            if weights[i][j] == 0:
                continue
            for k in range(size):
                if weights[i][k] != 0 and weights[k][j] != 0:
                    triangles.append((i, j, k))
    return triangles


def main(input_path: Path = INPUT_PATH) -> None:
    graph = read_gdf(input_path)
    # Triangle reports use node labels.
    labels = [graph.labels[node_id] for node_id in graph.node_ids]
    for i, j, k in find_triangles(graph.weight_matrix(0)):
        print(f"1: {labels[i]} 2: {labels[j]} 3: {labels[k]}")


if __name__ == "__main__":
    main()

"""CLI: test biconnectedness of each cluster graph and export its components."""

from __future__ import annotations

from pathlib import Path

import networkx as nx

from core.gdf_io import read_gdf

CLUSTER_DIR = Path("data/cluster")
OUTPUT_DIR = Path("biconnectedness")


def main(cluster_dir: Path = CLUSTER_DIR, output_dir: Path = OUTPUT_DIR) -> None:
    import xlwt

    output_dir.mkdir(parents=True, exist_ok=True)
    for gdf_path in sorted(cluster_dir.iterdir()):
        gdf = read_gdf(gdf_path)
        labels = gdf.labels

        network = nx.Graph()
        for node_id in gdf.node_ids:
            network.add_node(labels[node_id])
        for edge in gdf.edges:
            network.add_edge(labels[edge.source], labels[edge.target])

        components = list(nx.biconnected_components(network))
        print(
            f"{gdf_path.name}: biconnected={nx.is_biconnected(network)}, "
            f"components={len(components)}"
        )

        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet(gdf_path.stem)
        for column, component in enumerate(components):
            for row, label in enumerate(component):
                sheet.write(row, column, label)
        book.save(str(output_dir / f"{gdf_path.stem}.xls"))


if __name__ == "__main__":
    main()

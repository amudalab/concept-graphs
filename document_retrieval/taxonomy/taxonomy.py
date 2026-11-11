"""Build a taxonomy from clustered concept graphs.

Concepts are grouped into importance clusters (read from a spreadsheet).  For
consecutive clusters, each concept is linked to the nearest concept of the
cluster above it, using shortest paths in the concept graph.  Used by
``doc_ret_tax.py`` (per document), ``taxonomyKonEM.py`` and this module's CLI.
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple, Sequence

from core.gdf_io import GdfGraph, node_number, read_gdf, write_gdf
from analysis.shortest_paths import dijkstra, graph_from_gdf, path_length, path_to_root

HIERARCHY_PATH = Path("data/db/introhier.gdf")
CLUSTER_WORKBOOK_PATH = Path("data/Emnew.xlsx")
OUTPUT_GDF_PATH = Path("data/taxEM.gdf")
OUTPUT_EDGES_SHEET_PATH = Path("data/tax_edgesEM.xls")
CLUSTER_COUNT = 4
DEFAULT_CLUSTER_ORDER = [0, 1, 2, 3]


class ClusterEntry(NamedTuple):
    """One concept row of a cluster spreadsheet."""

    vertex_id: str
    label: str
    degree: str


def read_sheet_rows(workbook_path: str | Path, *, all_sheets: bool) -> list[list[list[object]]]:
    """Return the rows of each sheet of an ``.xlsx`` workbook.

    Numeric cells are returned as floats and empty cells as ``""`` so that
    ``str(value)`` matches what the original xlrd-based code produced.
    """
    import openpyxl

    workbook = openpyxl.load_workbook(str(workbook_path), data_only=True)
    worksheets = workbook.worksheets if all_sheets else workbook.worksheets[:1]
    sheets = []
    for worksheet in worksheets:
        rows: list[list[object]] = []
        for raw_row in worksheet.iter_rows(values_only=True):
            row: list[object] = []
            for value in raw_row:
                if value is None:
                    row.append("")
                elif isinstance(value, (int, float)) and not isinstance(value, bool):
                    row.append(float(value))
                else:
                    row.append(value)
            rows.append(row)
        sheets.append(rows)
    workbook.close()
    return sheets


def read_clusters(
    workbook_path: str | Path,
    cluster_count: int,
    *,
    all_sheets: bool,
    with_degree: bool,
) -> list[list[ClusterEntry]]:
    """Read cluster membership from a spreadsheet.

    Columns 1-2 hold the vertex id and label (apostrophes are removed from the
    label), column 3 optionally the degree, and the last column ``clusterN``.
    """
    clusters: list[list[ClusterEntry]] = [[] for _ in range(cluster_count)]
    for rows in read_sheet_rows(workbook_path, all_sheets=all_sheets):
        cluster_column = len(rows[0]) - 1
        for row in rows:
            entry = ClusterEntry(
                str(row[1]),
                str(row[2]).replace("'", ""),
                str(row[3]) if with_degree else "",
            )
            cluster_number = int(str(row[cluster_column]).replace("cluster", ""))
            clusters[cluster_number].append(entry)
    return clusters


def order_clusters_by_average_degree(clusters: Sequence[Sequence[ClusterEntry]]) -> list[int]:
    """Return cluster indices from highest to lowest average concept degree."""
    average_degree = []
    for cluster in clusters:
        total = sum(int(float(entry.degree)) for entry in cluster)
        average_degree.append(1.0 * total / len(cluster))
    ascending = sorted(average_degree)
    order = [average_degree.index(ascending[i]) for i in range(len(clusters))]
    return order[::-1]


class TaxonomyBuilder:
    """Accumulates taxonomy edges (child -> parent) over one or more cluster sets."""

    def __init__(self, hierarchy: GdfGraph) -> None:
        self.hierarchy = hierarchy
        self._graph = graph_from_gdf(hierarchy)
        self._weights = {(e.source, e.target): e.weight for e in hierarchy.edges}
        size = hierarchy.node_count
        # Shortest-path cost between concepts, ``None`` where not computed.
        self._path_cost: list[list[float | None]] = [[None] * size for _ in range(size)]
        self.taxonomy: list[list[float | None]] = [[None] * size for _ in range(size)]

    def add_clusters(self, clusters: Sequence[Sequence[ClusterEntry]], order: Sequence[int]) -> None:
        """Link concepts of ``order[i+1]`` to their nearest concept in ``order[i]``.

        Each concept takes the lowest-cost shortest path to a concept of the
        cluster above it as its parent.  Concepts of the top cluster that were
        not chosen as anyone's parent are then linked to the nearest concept of
        the last cluster or of the linked top-cluster concepts.  A concept that
        Dijkstra cannot reach gets path cost 0, as in the original algorithm.
        """
        size = self.hierarchy.node_count
        targets: list[str] = []
        for level in range(len(order) - 1):
            roots = [entry.vertex_id for entry in clusters[order[level]]]
            targets = [entry.vertex_id for entry in clusters[order[level + 1]]]
            for root in roots:
                dijkstra(self._graph, self._graph.vertices[root])
                for target_id in targets:
                    target = self._graph.get_vertex(target_id)
                    if target is None:
                        continue
                    cost = path_length(path_to_root(target), self._weights)
                    self._path_cost[node_number(target_id)][node_number(root)] = cost

        for row in range(size):
            nearest = self._nearest_column(row)
            if nearest is not None:
                self.taxonomy[row][nearest] = self._path_cost[row][nearest]

        top_cluster = clusters[order[0]]
        unlinked_roots = [
            entry.vertex_id
            for entry in top_cluster
            if all(
                self.taxonomy[row][node_number(entry.vertex_id)] is None
                for row in range(size)
            )
        ]
        for entry in top_cluster:
            if entry.vertex_id not in unlinked_roots:
                targets.append(entry.vertex_id)
        for root in unlinked_roots:
            root_index = node_number(root)
            dijkstra(self._graph, self._graph.vertices[root])
            for target_id in targets:
                target = self._graph.vertices[target_id]
                cost = path_length(path_to_root(target), self._weights)
                self._path_cost[root_index][node_number(target_id)] = cost
            nearest = self._nearest_column(root_index)
            if nearest is None:
                raise ValueError(f"no taxonomy link found for {root}")
            self.taxonomy[root_index][nearest] = self._path_cost[root_index][nearest]

    def _nearest_column(self, row: int) -> int | None:
        """Column with the smallest computed path cost in ``row`` (first on ties)."""
        nearest: int | None = None
        nearest_cost = 0.0
        for col, cost in enumerate(self._path_cost[row]):
            if cost is None:
                continue
            if nearest is None or cost < nearest_cost:
                nearest = col
                nearest_cost = cost
        return nearest

    def edge_lines(self) -> list[str]:
        """Taxonomy edges formatted as GDF edge lines."""
        return [
            f"v{i},v{j},false,{cost},true"
            for i, row in enumerate(self.taxonomy)
            for j, cost in enumerate(row)
            if cost is not None
        ]

    def write_gdf(self, path: Path) -> None:
        """Write the taxonomy as a GDF using the hierarchy's node section."""
        write_gdf(path, self.hierarchy.node_section, self.edge_lines())

    def write_edge_sheet(self, path: Path) -> None:
        """Write the taxonomy edges as label pairs to an ``.xls`` spreadsheet."""
        import xlwt

        labels = self.hierarchy.labels
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet("Python Sheet 1")
        sheet.write(0, 0, "vertex 1")
        sheet.write(0, 1, "vertex 2")
        row_number = 1
        for i, row in enumerate(self.taxonomy):
            for j, cost in enumerate(row):
                if cost is not None:
                    sheet.write(row_number, 0, labels[f"v{i}"])
                    sheet.write(row_number, 1, labels[f"v{j}"])
                    row_number += 1
        path.parent.mkdir(parents=True, exist_ok=True)
        book.save(str(path))


def main(
    hierarchy_path: Path = HIERARCHY_PATH,
    workbook_path: Path = CLUSTER_WORKBOOK_PATH,
    output_gdf_path: Path = OUTPUT_GDF_PATH,
    output_sheet_path: Path = OUTPUT_EDGES_SHEET_PATH,
) -> None:
    builder = TaxonomyBuilder(read_gdf(hierarchy_path))
    clusters = read_clusters(
        workbook_path, CLUSTER_COUNT, all_sheets=True, with_degree=False
    )
    builder.add_clusters(clusters, DEFAULT_CLUSTER_ORDER)
    builder.write_gdf(output_gdf_path)
    builder.write_edge_sheet(output_sheet_path)


if __name__ == "__main__":
    main()

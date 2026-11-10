"""Adjacency matrix over the terms of a document's word graph.

The matrix is a dict-of-dicts keyed by term (``matrix[row_term][col_term]``)
whose cells are :class:`edge.Edge` objects.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Sequence

from core.edge import Edge
from core.gdf_io import write_gdf

DOC_GRAPH_DIR = Path("data/doc_graphs")
WORD_DISTANCE_SHEET = Path("data/wdco.xls")

# A position list is a sequence of (term, token_index) pairs in document order.
PositionList = Sequence[tuple[str, int]]

_DOC_GRAPH_EDGE_HEADER = "edgedef> node1,node2,directed,weight,labelvisible"


class AdjMatrix:
    """Term-by-term matrix of :class:`edge.Edge` cells for a text graph."""

    def __init__(self) -> None:
        self.gmatrix: dict[str, dict[str, Edge]] = {}

    def create_matrix(
        self, terms: Sequence[str], positions: PositionList, directed: bool
    ) -> dict[str, dict[str, Edge]]:
        """Build the matrix for ``terms`` from consecutive term positions.

        Each pair of consecutive, distinct terms in ``positions`` contributes
        their token distance to the edge between them (in both directions
        unless ``directed`` is true).
        """
        for row_term in terms:
            self.gmatrix[row_term] = {col_term: Edge() for col_term in terms}
        self._accumulate_distances(positions, directed, as_float=True)
        return self.gmatrix

    def update_matrix(
        self, terms: Sequence[str], positions: PositionList, directed: bool
    ) -> None:
        """Grow the matrix to cover ``terms`` and add a new document's positions.

        ``terms`` must start with the terms already present in the matrix, in
        their existing order, followed by any new terms.
        """
        initial_size = len(self.gmatrix)
        for index, row_term in enumerate(terms):
            if index >= initial_size:
                self.gmatrix[row_term] = {col_term: Edge() for col_term in terms}
            else:
                for col_index in range(initial_size, len(terms)):
                    self.gmatrix[row_term][terms[col_index]] = Edge()
        self._accumulate_distances(positions, directed, as_float=False)

    def _accumulate_distances(
        self, positions: PositionList, directed: bool, *, as_float: bool
    ) -> None:
        for i in range(len(positions) - 1):
            row_term, row_index = positions[i]
            col_term, col_index = positions[i + 1]
            if col_term == row_term:
                continue
            distance: float = col_index - row_index
            if as_float:
                distance = float(distance)
            self._record_distance(row_term, col_term, distance)
            if not directed:
                self._record_distance(col_term, row_term, distance)

    def _record_distance(self, row_term: str, col_term: str, distance: float) -> None:
        cell = self.gmatrix[row_term][col_term]
        if cell.update_count == 0:
            cell.weight = distance
        else:
            cell.add_weight(distance)
        cell.increment_update_count()

    def floyd_warshall(self, terms: Sequence[str]) -> dict[str, dict[str, float]]:
        """Return all-pairs shortest distances over ``terms`` (Floyd-Warshall)."""
        paths = {
            row: {col: self.gmatrix[row][col].weight for col in terms} for row in terms
        }
        for via in terms:
            for source in terms:
                for target in terms:
                    through = paths[source][via] + paths[via][target]
                    if paths[source][target] > through:
                        paths[source][target] = through
        return paths

    def get_max_update_count(self, terms: Sequence[str]) -> int:
        """Return the largest ``update_count`` among the edges between ``terms``."""
        max_count = 0
        for row_term in terms:
            for col_term in terms:
                count = self.gmatrix[row_term][col_term].update_count
                if count > max_count:
                    max_count = count
        return max_count

    def export_document_graph(
        self,
        terms: Sequence[str],
        title: str,
        graph_dir: Path = DOC_GRAPH_DIR,
        spreadsheet_path: Path = WORD_DISTANCE_SHEET,
    ) -> None:
        """Write ``<graph_dir>/<title>.gdf`` and the word-distance spreadsheet."""
        max_count = self.get_max_update_count(terms)
        self._write_word_distance_sheet(terms, spreadsheet_path)

        node_section = ["nodedef> name,label"]
        node_section.extend(f"v{i},{term}" for i, term in enumerate(terms))
        edge_lines = []
        for i, row_term in enumerate(terms):
            for j, col_term in enumerate(terms):
                cell = self.gmatrix[row_term][col_term]
                if cell.weight != math.inf:
                    weight = cell.normalized_weight(max_count)
                    edge_lines.append(f"v{i},v{j},false,{weight},true")
        write_gdf(
            graph_dir / f"{title}.gdf",
            node_section,
            edge_lines,
            edge_header=_DOC_GRAPH_EDGE_HEADER,
        )

    def _write_word_distance_sheet(
        self, terms: Sequence[str], spreadsheet_path: Path
    ) -> None:
        import xlwt

        max_count = self.get_max_update_count(terms)
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet("Python Sheet 1")
        for column, header in enumerate(
            ("node1", "node2", "word distance", "co-occurance", "heuristics")
        ):
            sheet.write(0, column, header)
        row = 1
        for row_term in terms:
            for col_term in terms:
                cell = self.gmatrix[row_term][col_term]
                if cell.weight != math.inf:
                    sheet.write(row, 0, row_term)
                    sheet.write(row, 1, col_term)
                    sheet.write(row, 2, cell.weight / (0.1 * cell.update_count))
                    sheet.write(row, 3, cell.update_count)
                    sheet.write(row, 4, cell.normalized_weight(max_count))
                    row += 1
        spreadsheet_path.parent.mkdir(parents=True, exist_ok=True)
        book.save(str(spreadsheet_path))

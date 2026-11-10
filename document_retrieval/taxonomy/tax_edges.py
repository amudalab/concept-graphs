"""CLI: export the K and EM taxonomies as (parent, child) label pairs to one workbook."""

from __future__ import annotations

from pathlib import Path

from core.gdf_io import read_gdf

TAXONOMY_SHEETS = (
    ("taxonomy for K", Path("data/taxK.gdf")),
    ("taxonomy for EM", Path("data/taxEM4.gdf")),
)
OUTPUT_PATH = Path("data/tax_edges.xls")


def main(output_path: Path = OUTPUT_PATH) -> None:
    import xlwt

    book = xlwt.Workbook(encoding="utf-8")
    for sheet_name, gdf_path in TAXONOMY_SHEETS:
        graph = read_gdf(gdf_path)
        sheet = book.add_sheet(sheet_name)
        sheet.write(0, 0, "vertex 1")
        sheet.write(0, 1, "vertex 2")
        for row, edge in enumerate(graph.edges, start=1):
            sheet.write(row, 0, graph.labels[edge.target])
            sheet.write(row, 1, graph.labels[edge.source])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    book.save(str(output_path))


if __name__ == "__main__":
    main()

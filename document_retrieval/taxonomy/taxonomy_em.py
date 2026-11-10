"""Build one combined taxonomy from several K/EM cluster workbooks.

Each workbook ``KEM<id>.xlsx`` is paired with a hand-chosen cluster order; the
edges found for every workbook accumulate into a single taxonomy.
"""

from __future__ import annotations

from pathlib import Path

from core.gdf_io import read_gdf
from taxonomy.taxonomy import HIERARCHY_PATH, TaxonomyBuilder, read_clusters

# Directory holding the KEM<id>.xlsx workbooks.
WORKBOOK_DIR = Path("C:/Users/Romauld/Desktop/EM4")
OUTPUT_PATH = Path("taxKEM.gdf")

# Workbook id -> cluster indices from the top of the taxonomy downwards.
CLUSTER_ORDERS: dict[str, list[int]] = {
    "40": [1, 0, 2, 3],
    "41": [3, 2, 1, 0],
    "42": [1, 3, 2, 0],
    "43": [0, 1],
    "44": [0, 3, 1, 2],
    "45": [1, 0, 2, 3],
    "47": [3, 0, 1, 2],
    "48": [0, 2, 1, 3],
    "49": [1, 2, 3, 0],
    "410": [3, 2, 0, 1],
    "411": [2, 0, 1, 3],
    "412": [2, 3, 1, 0],
    "413": [0, 2, 1],
}


def main(
    hierarchy_path: Path = HIERARCHY_PATH,
    workbook_dir: Path = WORKBOOK_DIR,
    output_path: Path = OUTPUT_PATH,
) -> None:
    builder = TaxonomyBuilder(read_gdf(hierarchy_path))
    for workbook_id, order in CLUSTER_ORDERS.items():
        clusters = read_clusters(
            workbook_dir / f"KEM{workbook_id}.xlsx",
            len(order),
            all_sheets=True,
            with_degree=False,
        )
        builder.add_clusters(clusters, order)
    builder.write_gdf(output_path)


if __name__ == "__main__":
    main()

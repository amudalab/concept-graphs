"""CLI: shortest-path tree rooted at a single node of the hierarchy graph."""

from __future__ import annotations

from pathlib import Path

from core.gdf_io import read_gdf
from analysis.shortest_paths import write_single_source_shortest_path_tree

INPUT_PATH = Path("data/db/introhier.gdf")
SOURCE_NODE = "v54"


def main(input_path: Path = INPUT_PATH, source_id: str = SOURCE_NODE) -> None:
    label = read_gdf(input_path).labels[source_id]
    write_single_source_shortest_path_tree(
        input_path, source_id, Path(f"comp_shortest_path_tree_from_{label}.gdf")
    )


if __name__ == "__main__":
    main()

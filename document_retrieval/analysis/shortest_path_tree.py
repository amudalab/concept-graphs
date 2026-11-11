"""CLI: shortest-path trees from every node of ``introhier1.gdf``."""

from __future__ import annotations

from pathlib import Path

from analysis.shortest_paths import write_all_pairs_shortest_path_trees

INPUT_PATH = Path("introhier1.gdf")
OUTPUT_DIR = Path("shortest_path_tree1")


def main(input_path: Path = INPUT_PATH, output_dir: Path = OUTPUT_DIR) -> None:
    write_all_pairs_shortest_path_trees(input_path, output_dir)


if __name__ == "__main__":
    main()

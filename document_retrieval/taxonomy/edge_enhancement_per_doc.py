"""Build an enhanced semantic net for every document graph.

For each ``data/doc_graphs/<name>`` the matching taxonomy
``data/taxonomies/tax<name>`` is used to scale edge weights (see
:mod:`edge_enhancement`), and the result is written to
``data/enhanced_semantic_nets/enhanced_semantic_net_<name>``.
"""

from __future__ import annotations

from pathlib import Path

from taxonomy.edge_enhancement import enhance_file

DOC_GRAPH_DIR = Path("data/doc_graphs")
TAXONOMY_DIR = Path("data/taxonomies")
OUTPUT_DIR = Path("data/enhanced_semantic_nets")


def main(
    doc_graph_dir: Path = DOC_GRAPH_DIR,
    taxonomy_dir: Path = TAXONOMY_DIR,
    output_dir: Path = OUTPUT_DIR,
) -> None:
    for graph_path in sorted(doc_graph_dir.iterdir()):
        print(graph_path.name)
        enhance_file(
            taxonomy_dir / f"tax{graph_path.name}",
            graph_path,
            output_dir / f"enhanced_semantic_net_{graph_path.name}",
        )


if __name__ == "__main__":
    main()

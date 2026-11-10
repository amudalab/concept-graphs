"""Load per-document keyphrases and build the global keyphrase vocabulary.

Groundwork for keyphrase subsumption (co-occurrence) analysis.  The original
script never populated its co-occurrence matrix, so only loading is provided.
"""

from __future__ import annotations

from pathlib import Path

KEYS_DIR = Path("data/keys")


def load_document_keys(keys_dir: Path = KEYS_DIR) -> list[list[str]]:
    """Return the unique, non-empty keyphrases of every document in ``keys_dir``."""
    documents = []
    for key_file in sorted(keys_dir.iterdir()):
        lines = key_file.read_text(encoding="utf-8").split("\n")
        documents.append(sorted({line for line in lines if line}))
    return documents


def build_vocabulary(documents: list[list[str]]) -> list[str]:
    """Return every keyphrase that occurs in at least one document, sorted."""
    return sorted({key for document in documents for key in document})


def main() -> None:
    documents = load_document_keys()
    vocabulary = build_vocabulary(documents)
    print(f"{len(documents)} documents, {len(vocabulary)} distinct keyphrases")


if __name__ == "__main__":
    main()

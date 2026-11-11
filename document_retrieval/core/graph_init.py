"""Build and grow the concept graph from keyphrase files and a corpus.

``initgraph`` builds the graph for a first document, ``populate`` folds in
further documents, and ``demo`` builds one graph per corpus document.  The
current graph is kept in module state and exposed through
:func:`get_matrix` / :func:`get_text`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import nltk

from core.adjacency import AdjMatrix
from core.text_model import Text

CORPUS_DIR = Path("data/corpus")
KEYS_DIR = Path("data/keys")
KEYWORDS_PATH = Path("data/keywords")

_current_text: Text | None = None
_current_matrix: AdjMatrix | None = None


def get_text() -> Text:
    """Return the :class:`Text` of the graph built by the last ``initgraph`` call."""
    if _current_text is None:
        raise RuntimeError("No graph has been built; call initgraph() first.")
    return _current_text


def get_matrix() -> AdjMatrix:
    """Return the matrix of the graph built by the last ``initgraph`` call."""
    if _current_matrix is None:
        raise RuntimeError("No graph has been built; call initgraph() first.")
    return _current_matrix


def initgraph(keyfile: str | Path, textfile: str | Path) -> list[str]:
    """Build a fresh graph from a keyphrase file and a document.

    Returns the sorted list of keyphrases that occur in the document.
    """
    global _current_text, _current_matrix

    raw_keys = Path(keyfile).read_text(encoding="utf-8").lower()
    text = Text(raw_keys)
    unique_lines = list(set(nltk.line_tokenize(raw_keys)))
    text.tokens = sorted(_strip_line_endings(unique_lines))
    matrix = text.create_graph(str(textfile))
    _current_text = text
    _current_matrix = matrix
    return text.tokens


def populate(keyfile: str, textfile: str) -> None:
    """Add a document to the current graph.

    ``keyfile`` and ``textfile`` are names relative to ``data/keys`` and
    ``data/corpus`` respectively.  Plural terms whose singular is also present
    are merged into the singular.
    """
    text = get_text()
    matrix = get_matrix()

    raw_keys = (KEYS_DIR / keyfile).read_text(encoding="utf-8").lower()
    new_terms = _strip_line_endings(nltk.line_tokenize(raw_keys))
    document_text = Text(raw_keys)
    document_text.tokens = new_terms

    if document_text.tokens:
        positions = document_text.update_graph(str(CORPUS_DIR / textfile))
        text.update_tokens(document_text.tokens)
        matrix.update_matrix(text.tokens, positions, False)
        text.tokens.sort()

    merged_plurals: list[str] = []
    for term in text.tokens:
        if term.endswith("s") and term[:-1] in text.tokens:
            singular = term[:-1]
            _merge_plural_into_singular(matrix, text.tokens, term, singular)
            merged_plurals.append(term)
    for term in merged_plurals:
        for other in text.tokens:
            del matrix.gmatrix[other][term]
    for term in merged_plurals:
        del matrix.gmatrix[term]
        text.tokens.remove(term)


def demo() -> None:
    """Build a graph for every corpus document and record the combined keywords."""
    all_keywords: set[str] = set()
    for corpus_file in sorted(CORPUS_DIR.glob("*.txt")):
        key_file = KEYS_DIR / f"{corpus_file.stem}.key"
        initgraph(key_file, corpus_file)
        all_keywords.update(get_text().tokens)
        get_matrix().export_document_graph(get_text().tokens, corpus_file.stem)

    KEYWORDS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with KEYWORDS_PATH.open("w", encoding="utf-8") as handle:
        for keyword in sorted(all_keywords):
            handle.write(keyword + "\n")


def _merge_plural_into_singular(
    matrix: AdjMatrix, terms: Sequence[str], plural: str, singular: str
) -> None:
    """Fold the edges of ``plural`` into those of ``singular`` (both directions)."""
    cells = matrix.gmatrix
    for other in terms:
        plural_cell = cells[other][plural]
        if plural_cell.weight == float("inf"):
            continue
        singular_cell = cells[other][singular]
        if singular_cell.weight != float("inf"):
            singular_cell.weight += plural_cell.weight
            singular_cell.update_count += plural_cell.update_count
        else:
            singular_cell.weight = plural_cell.weight
            singular_cell.update_count = plural_cell.update_count
        cells[singular][other].weight = singular_cell.weight
        cells[singular][other].update_count = singular_cell.update_count


def _strip_line_endings(lines: Sequence[str]) -> list[str]:
    """Strip trailing carriage returns, spaces and tabs from each line."""
    return [line.rstrip("\r").rstrip(" \t") for line in lines]


if __name__ == "__main__":
    demo()

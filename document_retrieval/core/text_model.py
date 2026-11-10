"""Token container that owns concept-graph construction for one text."""

from __future__ import annotations

from typing import Iterable, Sequence

from core.adjacency import AdjMatrix
from core.preprocessing import remove_stopword
from core.text_graph import Position, create_graph, update_graph


class Text:
    """A sequence of terms plus helpers to build and update term graphs."""

    def __init__(self, tokens: Sequence[str], name: str | None = None) -> None:
        self.tokens: list[str] = list(tokens)
        if name:
            self.name = name
        elif "]" in self.tokens[:20]:
            end = self.tokens[:20].index("]")
            self.name = " ".join(map(str, self.tokens[1:end]))
        else:
            self.name = " ".join(map(str, self.tokens[:8])) + "..."

    def create_graph(self, filename: str) -> AdjMatrix:
        """Build the term graph for the document at ``filename``."""
        return create_graph(self, filename)

    def update_graph(self, filename: str) -> list[Position]:
        """Return term positions for ``filename`` (see :func:`textgraph.update_graph`)."""
        return update_graph(self, filename)

    def remove_stopword(self) -> list[str]:
        """Return tokens with English stopwords and tokens of 3 chars or fewer removed."""
        return remove_stopword(self.tokens)

    def index(self, word: str) -> int:
        """Return the index of the first occurrence of ``word``."""
        return self.tokens.index(word)

    def update_tokens(self, new_tokens: Iterable[str]) -> None:
        """Append any previously unseen tokens (unique, sorted order)."""
        for token in sorted(set(new_tokens)):
            if token not in self.tokens:
                self.tokens.append(token)

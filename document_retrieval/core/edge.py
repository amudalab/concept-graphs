"""Edge object for the word co-occurrence graph.

An :class:`Edge` accumulates the summed word distance between two terms and
the number of times that distance was observed.
"""

from __future__ import annotations

import math


class Edge:
    """Weighted edge between two terms in a text graph.

    ``weight`` holds the *sum* of the observed word distances (``math.inf``
    until the first observation) and ``update_count`` the number of
    observations that contributed to it.
    """

    def __init__(self) -> None:
        self.weight: float = math.inf
        self.update_count: int = 0

    def increment_update_count(self) -> None:
        """Record one more observation for this edge."""
        self.update_count += 1

    def add_weight(self, distance: float) -> None:
        """Add ``distance`` to the accumulated weight."""
        self.weight = self.weight + distance

    def normalized_weight(self, max_update_count: int) -> float:
        """Return the heuristic weight used when writing graphs to disk.

        The accumulated distance is scaled by how often the edge was seen
        relative to the most frequently seen edge in the graph.
        """
        return (self.weight * (max_update_count - self.update_count)) / (
            (self.update_count * 1.0) * max_update_count
        )

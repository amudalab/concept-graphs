"""File IO helpers for feature pipelines."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Tuple


def read_text(path: Path | str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def read_lines(path: Path | str) -> List[str]:
    return [
        line.rstrip("\n\r")
        for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
        if line.strip()
    ]


def write_score_file(
    path: Path | str,
    scores: Mapping[str, float],
    *,
    normalize: bool = False,
) -> None:
    """Write ``phrase::score`` lines sorted by score descending."""
    items: List[Tuple[str, float]] = sorted(
        scores.items(), key=lambda item: item[1], reverse=True
    )
    if normalize and items:
        peak = items[0][1]
        if peak:
            items = [(phrase, value / peak) for phrase, value in items]

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        "".join(f"{phrase}::{score}\n" for phrase, score in items),
        encoding="utf-8",
    )


def write_lines(path: Path | str, lines: Iterable[str]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        "".join(f"{line}\n" for line in lines),
        encoding="utf-8",
    )

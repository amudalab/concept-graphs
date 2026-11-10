"""Unified command-line interface for keyphrase_extraction."""

from __future__ import annotations

import argparse
from typing import Callable, Dict, List, Sequence

from features import cscore, cue, dispersion, feature_table, local_span, tfidf
from pipeline import main as pipeline_main
from preprocess import ngrams, pos_tag

Command = Callable[[List[str] | None], int]

COMMANDS: Dict[str, Command] = {
    "pos": pos_tag.main,
    "grams": ngrams.main,
    "cscore": cscore.main,
    "cue": cue.main,
    "localspan": local_span.main,
    "dispersion": dispersion.main,
    "tfidf": tfidf.main,
    "write": feature_table.main,
    "pipeline": pipeline_main,
}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="keyphrase_extraction",
        description="Concept-graphs keyphrase feature toolkit (Python 3).",
    )
    parser.add_argument(
        "command",
        choices=sorted(COMMANDS),
        help="Subcommand to run",
    )
    ns, remainder = parser.parse_known_args(argv)
    return int(COMMANDS[ns.command](remainder))


if __name__ == "__main__":
    raise SystemExit(main())

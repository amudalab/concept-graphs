"""End-to-end keyphrase feature pipeline for a single lecture."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Sequence

from features import cscore, cue, dispersion, feature_table, local_span, tfidf
from preprocess import ngrams, pos_tag


DEFAULT_FEATURES: Sequence[str] = (
    "cscore",
    "localspan",
    "cuewords",
    "dispersion",
    "tfidf",
)
DEFAULT_EXTS: Sequence[str] = (
    "_cscore.txt",
    "_localspan.txt",
    "_cue.txt",
    "_disp.txt",
    "_tfidf.txt",
)


def run_pipeline(
    lecture: str,
    *,
    stemmer: str = "none",
    max_gram: int = 3,
    enable_pos: bool = True,
    pos_filter: Path | None = None,
) -> Path:
    """Run preprocess → features → merged table. Returns the ``.tab`` path."""
    pos_tag.process_lecture(lecture, stemmer, enable_pos=enable_pos)
    ngrams.process_lecture(lecture, max_gram, stemmer, pos_filter=pos_filter)
    cscore.score_file(lecture)
    local_span.score_file(lecture)
    cue.score_file(lecture, stemmer, max_gram)
    dispersion.score_file(lecture)
    tfidf.score_lecture(lecture, stemmer, max_gram)
    return feature_table.build_feature_table(lecture, DEFAULT_FEATURES, DEFAULT_EXTS)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the full keyphrase feature pipeline.")
    parser.add_argument("lecture")
    parser.add_argument("--stemmer", default="none")
    parser.add_argument("--max-gram", type=int, default=3)
    parser.add_argument("--pos", choices=("enable", "disable"), default="enable")
    parser.add_argument("--pos-filter", default=None)
    args = parser.parse_args(argv)
    filter_path = Path(args.pos_filter) if args.pos_filter else None
    path = run_pipeline(
        args.lecture,
        stemmer=args.stemmer,
        max_gram=args.max_gram,
        enable_pos=args.pos == "enable",
        pos_filter=filter_path,
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

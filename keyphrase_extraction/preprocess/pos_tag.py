"""POS-tag (optional) and stem a transcript into tagged/untagged outputs."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import nltk

from _internal.paths import OUTPUT_DIR, TRANSCRIPTS_DIR, lecture_stem
from _internal.stemming import StemmerName, parse_stemmer_name, stem_token
from _internal.text import clean_token
from _internal.io import write_lines


def _tokenize_transcript(text: str) -> List[str]:
    return text.split()


def preprocess_tokens(
    raw_tokens: Sequence[str],
    stemmer_name: StemmerName,
) -> Tuple[List[str], Dict[str, str]]:
    """Return stemmed tokens and a stem→surface map."""
    stemmed: List[str] = []
    stem_to_root: Dict[str, str] = {}
    for raw in raw_tokens:
        surface = clean_token(raw)
        if not surface:
            continue
        root = stem_token(surface, stemmer_name)
        stem_to_root[root] = surface
        stemmed.append(root)
    return stemmed, stem_to_root


def tag_tokens(
    tokens: Sequence[str], *, enabled: bool
) -> List[Tuple[str, str]]:
    if enabled:
        return list(nltk.pos_tag(list(tokens)))
    return [(token, "NONE") for token in tokens]


def process_lecture(
    lecture: str,
    stemmer_name: str | StemmerName,
    *,
    enable_pos: bool,
    transcript_dir: Path = TRANSCRIPTS_DIR,
    output_dir: Path = OUTPUT_DIR,
) -> Tuple[Path, Path]:
    name = parse_stemmer_name(stemmer_name) if isinstance(stemmer_name, str) else stemmer_name
    stem = lecture_stem(lecture)
    source = transcript_dir / Path(lecture).name
    if not source.exists():
        # allow bare stem
        source = transcript_dir / f"{stem}.txt"
    raw = source.read_text(encoding="utf-8", errors="replace")
    stemmed, stem_to_root = preprocess_tokens(_tokenize_transcript(raw), name)
    tagged = tag_tokens(stemmed, enabled=enable_pos)

    tagged_path = output_dir / f"{stem}_tagged.txt"
    untagged_path = output_dir / f"{stem}_untagged.txt"
    root_path = output_dir / f"{stem}_root.txt"
    output_dir.mkdir(parents=True, exist_ok=True)

    tagged_path.write_text(
        " ".join(f"{token}/{tag}/{token}" for token, tag in tagged) + "\n",
        encoding="utf-8",
    )
    untagged_path.write_text(" ".join(stemmed) + "\n", encoding="utf-8")
    write_lines(root_path, (f"{stem_}::{root}" for stem_, root in stem_to_root.items()))
    return tagged_path, untagged_path


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="POS-tag and stem a transcript.")
    parser.add_argument("lecture")
    parser.add_argument("stemmer")
    parser.add_argument(
        "pos_status",
        choices=("enable", "disable", "none"),
        help="enable = run NLTK POS tagger",
    )
    args = parser.parse_args(argv)
    enable = args.pos_status == "enable"
    tagged, untagged = process_lecture(args.lecture, args.stemmer, enable_pos=enable)
    print(tagged)
    print(untagged)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

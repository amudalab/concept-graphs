"""Extract candidate n-grams from a POS-tagged lecture file."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set

from lexicons.stopwords import stemmed_stopwords
from _internal.io import write_lines
from _internal.paths import CONFIG_DIR, OUTPUT_DIR, lecture_stem
from _internal.stemming import StemmerName, parse_stemmer_name
from _internal.text import is_number, surface_from_tagged


def _load_pos_allowlist(path: Path | None) -> Set[str] | None:
    if path is None:
        return None
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def extract_ngrams(
    tagged_tokens: Sequence[str],
    *,
    max_gram: int,
    stopwords: Iterable[str],
    allowed_pos: Set[str] | None = None,
) -> Dict[str, int]:
    banned = set(stopwords)
    counts: Counter[str] = Counter()
    for length in range(1, max_gram + 1):
        for start in range(0, len(tagged_tokens) - length + 1):
            window = tagged_tokens[start : start + length]
            surfaces: List[str] = []
            tags: List[str] = []
            valid = True
            for token in window:
                parts = token.split("/")
                surface = parts[0]
                tag = parts[1] if len(parts) > 1 else "NONE"
                if is_number(surface) or not surface.strip():
                    valid = False
                    break
                surfaces.append(surface)
                tags.append(tag)
            if not valid:
                continue
            if allowed_pos is not None and any(tag not in allowed_pos for tag in tags):
                continue
            if (
                surfaces[0] in banned
                or surfaces[-1] in banned
                or len(surfaces[0]) <= 2
                or len(surfaces[-1]) <= 2
            ):
                continue
            counts[" ".join(surfaces)] += 1
    return dict(counts)


def process_lecture(
    lecture: str,
    max_gram: int,
    stemmer_name: str | StemmerName,
    *,
    pos_filter: Path | None = None,
    output_dir: Path = OUTPUT_DIR,
) -> Path:
    name = parse_stemmer_name(stemmer_name) if isinstance(stemmer_name, str) else stemmer_name
    stem = lecture_stem(lecture)
    tagged_path = output_dir / f"{stem}_tagged.txt"
    tokens = tagged_path.read_text(encoding="utf-8", errors="replace").split()
    allowlist = _load_pos_allowlist(pos_filter)
    grams = extract_ngrams(
        tokens,
        max_gram=max_gram,
        stopwords=stemmed_stopwords(name),
        allowed_pos=allowlist,
    )
    destination = output_dir / f"{stem}_grams.txt"
    write_lines(destination, sorted(grams))
    return destination


def main(argv: List[str] | None = None) -> int:
    """
    Supported call shapes (legacy shell scripts):

    - ``grams.py LECTURE MAX_GRAM STEMMER``
    - ``grams_pos.py LECTURE MAX_GRAM POS_FILTER STEMMER``
    """
    parser = argparse.ArgumentParser(description="Extract candidate n-grams.")
    parser.add_argument("lecture")
    parser.add_argument("max_gram", type=int)
    parser.add_argument("pos_filter_or_stemmer")
    parser.add_argument("stemmer", nargs="?", default=None)
    args = parser.parse_args(argv)

    if args.stemmer is None:
        pos_filter: Path | None = None
        stemmer = args.pos_filter_or_stemmer
    else:
        stemmer = args.stemmer
        raw = args.pos_filter_or_stemmer
        if raw in {"none", "None", ""}:
            pos_filter = None
        elif raw == "default_posfilter":
            pos_filter = CONFIG_DIR / "pos_filter.txt"
        else:
            pos_filter = Path(raw)

    print(process_lecture(args.lecture, args.max_gram, stemmer, pos_filter=pos_filter))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Merge per-feature score files into a single Orange/sklearn-friendly table."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence

from _internal.io import read_lines
from _internal.paths import OUTPUT_DIR, lecture_stem


def _load_scores(path: Path) -> Dict[str, str]:
    scores: Dict[str, str] = {}
    if not path.exists():
        return scores
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "::" not in line:
            continue
        phrase, value = line.split("::", 1)
        scores[phrase] = value
    return scores


def build_feature_table(
    lecture: str,
    feature_names: Sequence[str],
    feature_exts: Sequence[str],
    *,
    output_dir: Path = OUTPUT_DIR,
    stem_to_root: Mapping[str, str] | None = None,
) -> Path:
    if len(feature_names) != len(feature_exts):
        raise ValueError("feature_names and feature_exts must have the same length")

    stem = lecture_stem(lecture)
    grams = read_lines(output_dir / f"{stem}_grams.txt")
    # Optional video grams
    video_grams_path = output_dir / f"{stem}_vgrams.txt"
    if video_grams_path.exists():
        grams = list(dict.fromkeys(grams + read_lines(video_grams_path)))

    per_feature: Dict[str, Dict[str, str]] = {}
    for name, ext in zip(feature_names, feature_exts):
        per_feature[name] = _load_scores(output_dir / f"{stem}{ext}")

    roots = dict(stem_to_root or {})
    root_map_path = output_dir / f"{stem}_root.txt"
    if root_map_path.exists():
        for line in read_lines(root_map_path):
            if "::" in line:
                stemmed, root = line.split("::", 1)
                roots[stemmed] = root

    destination = output_dir / f"{stem}.tab"
    lines: List[str] = []
    header = ["keyphrase", *feature_names, "keyword"]
    lines.append("\t".join(header))
    lines.append("\t".join(["d", *["c"] * len(feature_names), "d"]))
    lines.append("\t".join(["m", *[""] * len(feature_names), "class"]))

    for gram in grams:
        display = " ".join(roots.get(token, token) for token in gram.split())
        values = [per_feature[name].get(gram, "0.0") for name in feature_names]
        lines.append("\t".join([display, *values, "False"]))

    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return destination


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Merge feature score files into a .tab table.")
    parser.add_argument("lecture")
    parser.add_argument(
        "feature_list",
        help="Comma-separated feature names, e.g. cscore,localspan,cuewords,dispersion,tfidf",
    )
    parser.add_argument(
        "feature_ext",
        help="Comma-separated file suffixes, e.g. _cscore.txt,_localspan.txt,...",
    )
    parser.add_argument("stemmer", nargs="?", default="none")
    args = parser.parse_args(argv)
    names = [part.strip() for part in args.feature_list.split(",") if part.strip()]
    exts = [part.strip() for part in args.feature_ext.split(",") if part.strip()]
    print(build_feature_table(args.lecture, names, exts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

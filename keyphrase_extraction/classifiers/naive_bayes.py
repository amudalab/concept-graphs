"""Naive Bayes keyphrase classifier (scikit-learn; replaces Orange 2)."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import KBinsDiscretizer

from _internal.paths import OUTPUT_DIR, TRAINING_DATA_DIR, lecture_stem


def _parse_tab(path: Path) -> Tuple[List[str], np.ndarray, np.ndarray, List[str]]:
    """
    Parse the legacy 3-header-row ``.tab`` format.

    Returns feature names, X, y (1=True keyword), and keyphrase strings.
    """
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if len(lines) < 4:
        raise ValueError(f"{path} has no data rows")
    headers = [part.strip() for part in lines[0].split("\t")]
    feature_names = [
        name for name in headers if name not in {"keyphrase", "keyword", ""}
    ]
    phrases: List[str] = []
    rows: List[List[float]] = []
    labels: List[int] = []
    for line in lines[3:]:
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        phrase = parts[0].strip()
        feature_values = []
        for index, name in enumerate(feature_names, start=1):
            raw = parts[index].strip() if index < len(parts) else "0.0"
            try:
                feature_values.append(float(raw))
            except ValueError:
                feature_values.append(0.0)
        label_raw = parts[-1].strip().lower() if parts else "false"
        labels.append(1 if label_raw in {"true", "1", "yes"} else 0)
        phrases.append(phrase)
        rows.append(feature_values)
    return feature_names, np.asarray(rows, dtype=float), np.asarray(labels), phrases


class KeyphraseNaiveBayes:
    """Discretize continuous features then fit Gaussian Naive Bayes."""

    def __init__(self, n_bins: int = 5) -> None:
        self._discretizer = KBinsDiscretizer(
            n_bins=n_bins, encode="ordinal", strategy="quantile"
        )
        self._model = GaussianNB()
        self.feature_names: List[str] = []

    def fit(self, path: Path) -> "KeyphraseNaiveBayes":
        self.feature_names, features, labels, _ = _parse_tab(path)
        if len(features) == 0:
            raise ValueError(f"No training rows in {path}")
        transformed = self._discretizer.fit_transform(features)
        self._model.fit(transformed, labels)
        return self

    def predict_phrases(self, path: Path) -> List[str]:
        _, features, _, phrases = _parse_tab(path)
        if len(features) == 0:
            return []
        transformed = self._discretizer.transform(features)
        predictions = self._model.predict(transformed)
        return [phrase for phrase, label in zip(phrases, predictions) if label == 1]


def classify_lecture(
    training_tab: str,
    lecture: str,
    *,
    training_dir: Path = TRAINING_DATA_DIR,
    output_dir: Path = OUTPUT_DIR,
) -> Path:
    stem = lecture_stem(lecture)
    model = KeyphraseNaiveBayes().fit(training_dir / Path(training_tab).name)
    test_tab = output_dir / f"{stem}.tab"
    predicted = model.predict_phrases(test_tab)
    destination = output_dir / f"{stem}.txt"
    destination.write_text("".join(f"{phrase}\n" for phrase in predicted), encoding="utf-8")
    return destination


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Classify keyphrases with scikit-learn Naive Bayes."
    )
    parser.add_argument("training_tab", help="Training .tab inside data/training_data")
    parser.add_argument("lecture", help="Lecture stem or .txt name")
    args = parser.parse_args(argv)
    print(classify_lecture(args.training_tab, args.lecture))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

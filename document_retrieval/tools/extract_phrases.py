"""Turn key-phrase score files into per-document keyphrase lists.

Reads the TF-IDF scored phrases in ``data/key_phrase_scores`` and writes

* ``data/keys/<doc>``      - the surviving phrases/words of each document,
* ``data/filewords(om)3``  - ``<doc>>phrase1,phrase2,...`` for every document,
* ``data/nwdb``            - every phrase/word over all documents.

A phrase survives when its best TF-IDF score exceeds ``TFIDF_CUTOFF_RATIO``
times the best score overall and it occurs at least twice in the document.
"""

from __future__ import annotations

import operator
from pathlib import Path
from typing import Iterator

import nltk
from nltk.corpus import stopwords

from core.text_graph import find_phrase_positions

SCORES_DIR = Path("data/key_phrase_scores")
KEYS_DIR = Path("data/keys")
CORPUS_DIR = Path("data/corpus")
FILEWORDS_PATH = Path("data/filewords(om)3")
VOCABULARY_PATH = Path("data/nwdb")

TFIDF_CUTOFF_RATIO = 0.1
_EXCLUDED_CHARACTERS = "=:%;><.,"
_HEADER_LINE_COUNT = 2
_TOKEN_PATTERN = r"[\w']+"


def _read_scored_phrases(score_path: Path) -> Iterator[tuple[str, float]]:
    """Yield ``(phrase, tfidf)`` for each usable data row of a score file.

    The first two lines are headers.  The phrase is every token of a row except
    the trailing score columns; rows whose phrase has punctuation are skipped.
    """
    with score_path.open(encoding="utf-8") as handle:
        rows = [line.strip().lower().split() for line in handle]
    extra_columns = len(rows[0]) - 1
    tfidf_column = rows[0].index("tfidf")
    for line_number, tokens in enumerate(rows):
        if line_number < _HEADER_LINE_COUNT:
            continue
        phrase_length = len(tokens) - extra_columns
        phrase = " ".join(tokens[: max(phrase_length, 0)])
        if any(char in phrase for char in _EXCLUDED_CHARACTERS):
            continue
        yield phrase, float(tokens[phrase_length + tfidf_column])


def _best_tfidf_scores(score_files: list[Path]) -> dict[str, float]:
    """Return the highest TF-IDF score seen for each phrase over all files."""
    best: dict[str, float] = {}
    for score_path in score_files:
        for phrase, score in _read_scored_phrases(score_path):
            if phrase not in best or best[phrase] < score:
                best[phrase] = score
    return best


def _document_terms(
    phrases: list[str], corpus_path: Path, stop_words: list[str]
) -> list[str]:
    """Return the sorted phrases of a document plus the content words they contain."""
    document_tokens = nltk.regexp_tokenize(
        corpus_path.read_text(encoding="utf-8", errors="replace").lower(),
        _TOKEN_PATTERN,
    )
    positions_by_term: dict[str, list[tuple[str, int]]] = {}
    unmatched: list[str] = []
    for phrase in phrases:
        positions = find_phrase_positions(document_tokens, phrase, phrases)
        if not positions:
            unmatched.append(phrase)
            continue
        canonical = positions[0][0]
        if canonical in positions_by_term:
            for position in positions:
                if position not in positions_by_term[canonical]:
                    positions_by_term[canonical].append(position)
        else:
            positions_by_term[canonical] = positions

    for term, positions in positions_by_term.items():
        if len(positions) < 2:
            phrases.remove(term)
    for phrase in unmatched:
        phrases.remove(phrase)

    words = []
    for phrase in phrases:
        for word in nltk.regexp_tokenize(phrase, _TOKEN_PATTERN):
            if word not in stop_words and len(word) > 1 and not word.isdigit():
                words.append(word)
    return sorted(set(phrases) | set(words))


def main(
    scores_dir: Path = SCORES_DIR,
    keys_dir: Path = KEYS_DIR,
    corpus_dir: Path = CORPUS_DIR,
    filewords_path: Path = FILEWORDS_PATH,
    vocabulary_path: Path = VOCABULARY_PATH,
) -> None:
    score_files = sorted(path for path in scores_dir.iterdir() if path.is_file())
    best_scores = _best_tfidf_scores(score_files)
    ranked = sorted(best_scores.items(), key=operator.itemgetter(1), reverse=True)
    cut_off = float(ranked[0][1]) * TFIDF_CUTOFF_RATIO
    stop_words = stopwords.words("english")

    keys_dir.mkdir(parents=True, exist_ok=True)
    vocabulary: set[str] = set()
    with filewords_path.open("w", encoding="utf-8") as filewords:
        for score_path in score_files:
            document = score_path.stem
            phrases = [
                phrase
                for phrase, _ in _read_scored_phrases(score_path)
                if best_scores[phrase] > cut_off
            ]
            terms = _document_terms(phrases, corpus_dir / f"{document}.txt", stop_words)
            vocabulary.update(terms)
            filewords.write(f"{document}>{','.join(terms)}\n")
            (keys_dir / document).write_text(
                "".join(term + "\n" for term in terms), encoding="utf-8"
            )

    with vocabulary_path.open("w", encoding="utf-8") as handle:
        for term in sorted(vocabulary):
            handle.write(term + "\n")


if __name__ == "__main__":
    main()

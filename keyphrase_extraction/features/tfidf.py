"""Corpus-aware TF–IDF scores for candidate n-grams."""

from __future__ import annotations

import argparse
import math
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from lexicons.stopwords import stemmed_stopwords
from _internal.io import write_score_file
from _internal.paths import OUTPUT_DIR, TRANSCRIPTS_DIR, lecture_stem
from _internal.stemming import StemmerName, parse_stemmer_name, stem_phrase
from _internal.text import clean_phrase, is_number, surface_from_tagged


class DocumentGrams:
    """N-gram frequency table for a single transcript."""

    def __init__(
        self,
        name: str,
        tokens: Sequence[str],
        *,
        max_gram: int,
        stopwords: Iterable[str],
        stemmer_name: StemmerName,
    ) -> None:
        self.name = name
        self.size = len(tokens)
        self.grams: Counter[str] = Counter()
        banned = set(stopwords)
        for start in range(len(tokens)):
            for length in range(1, max_gram):
                end = start + length
                if end > len(tokens):
                    break
                surfaces = [surface_from_tagged(tok) for tok in tokens[start:end]]
                if any(is_number(token) or not token.strip() for token in surfaces):
                    continue
                phrase = clean_phrase(" ".join(surfaces))
                words = phrase.split()
                if (
                    not words
                    or words[0] in banned
                    or words[-1] in banned
                    or len(words[0]) <= 2
                    or len(words[-1]) <= 2
                ):
                    continue
                self.grams[stem_phrase(phrase, stemmer_name)] += 1


class TfidfScorer:
    """TF–IDF across a collection of :class:`DocumentGrams`."""

    def __init__(self, documents: Sequence[DocumentGrams]) -> None:
        self._documents = list(documents)

    def scores_for(self, document: DocumentGrams) -> Dict[str, float]:
        corpus_size = len(self._documents)
        result: Dict[str, float] = {}
        if document.size == 0 or corpus_size == 0:
            return result
        for phrase, tf in document.grams.items():
            document_frequency = sum(
                1 for other in self._documents if phrase in other.grams
            )
            if document_frequency == 0:
                continue
            idf = math.log(corpus_size / float(document_frequency))
            result[phrase] = len(phrase.split()) * (tf / float(document.size)) * idf
        return result


def score_lecture(
    lecture: str,
    stemmer_name: str | StemmerName,
    max_gram: int,
    *,
    transcript_dir: Path = TRANSCRIPTS_DIR,
    output_dir: Path = OUTPUT_DIR,
) -> Path:
    name = parse_stemmer_name(stemmer_name) if isinstance(stemmer_name, str) else stemmer_name
    stopwords = stemmed_stopwords(name)
    documents: List[DocumentGrams] = []
    for path in sorted(transcript_dir.glob("*.txt")):
        tokens = path.read_text(encoding="utf-8", errors="replace").split()
        documents.append(
            DocumentGrams(
                path.name,
                tokens,
                max_gram=max_gram,
                stopwords=stopwords,
                stemmer_name=name,
            )
        )

    target_name = Path(lecture).name
    scorer = TfidfScorer(documents)
    target = next(doc for doc in documents if doc.name == target_name)
    destination = output_dir / f"{lecture_stem(target_name)}_tfidf.txt"
    write_score_file(destination, scorer.scores_for(target))
    return destination


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute TF–IDF feature scores.")
    parser.add_argument("stemmer")
    parser.add_argument("max_gram", type=int)
    parser.add_argument("lecture", help="Transcript filename inside data/transcripts")
    args = parser.parse_args(argv)
    print(score_lecture(args.lecture, args.stemmer, args.max_gram))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

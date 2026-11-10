# Concept Graphs

Algorithms and tools for building **concept graphs** from educational video
transcripts and documents: keyphrase extraction, taxonomy / semantic-network
construction, document retrieval over those graphs, and a Processing-based
explorer UI.

> **Runtime note.** This repository targets **Python 2.7**. A large share of the
> scripts use Python 2 `print` statements and classic `/` integer division.
> Porting to Python 3 is intentionally deferred so numeric results can be
> validated separately.

## Repository layout

```
concept-graphs/
├── keyphrase_extraction/       # Audio/video keyphrase feature pipeline + ML
├── fast_keyphrase_extraction/  # Streamlined keyphrase batch runner
├── document_retrieval/         # Concept-graph construction & retrieval
├── google_pdf_search/          # Google Custom Search → PDF ingest helpers
├── visualization/
│   └── concept_explorer/       # Processing (Java mode) concept browser
├── docs/                       # Project documentation (PDF / ODT / PS)
├── requirements.txt
└── LICENSE
```

| Module | Purpose |
|--------|---------|
| [`keyphrase_extraction/`](keyphrase_extraction/) | Feature extraction (TF–IDF, cue words, dispersion, …), Naive Bayes ranking, experiment shell scripts |
| [`fast_keyphrase_extraction/`](fast_keyphrase_extraction/) | Compact automate-and-run variant of the same pipeline |
| [`document_retrieval/`](document_retrieval/) | Build adjacency / taxonomy graphs from keyphrases; bag-of-words and graph-enhanced retrieval; small `web.py` demos |
| [`google_pdf_search/`](google_pdf_search/) | Query Google Custom Search for PDFs and convert them for keyphrase input |
| [`visualization/concept_explorer/`](visualization/concept_explorer/) | Processing sketch for browsing concept subgraphs |

## Setup

```bash
# Prefer a Python 2.7 virtualenv
virtualenv -p python2.7 .venv
source .venv/bin/activate
pip install -r requirements.txt

# NLTK resources used by the pipelines (not vendored in the repo)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

Orange 2.x is required for `keyphrase_extraction/ml/naive_bayes/` and is not on
modern PyPI — install from the [Orange 2](https://orange.biolab.si/orange2/)
distribution if you need those classifiers.

## How to run (high level)

Always run commands from the **module root** so relative `data/` paths resolve.

```bash
# Keyphrase features for a transcript
cd keyphrase_extraction
sh scripts/grams.sh ds1.txt 3 config/pos_filter.txt none
sh scripts/tfidf.sh none 3 ds1.txt
# …or the combined demo pipeline:
sh scripts/keyphraseExt.sh

# Fast batch runner
cd ../fast_keyphrase_extraction
python automate.py

# Document retrieval / graph build (examples)
cd ../document_retrieval
python graph_init.py          # builds graphs from data/keys + data/corpus
python doc_ret_bag_of_words.py

# Google PDF search (credentials via env — never commit keys)
cd ../google_pdf_search
export GOOGLE_API_KEY=...
export GOOGLE_CSE_ID=...
python gcs.py
```

Open `visualization/concept_explorer/` in the [Processing](https://processing.org/)
IDE (Java mode). Media and JSON live under that sketch’s `data/` folder.

See each module’s `README.md` for details.

## Design notes from the restructure

- Folder and file names are snake_case; spaces and typos in paths are gone.
- Data (transcripts, corpora, graphs, generated features) lives under each
  module’s `data/` directory; source code is separate from data.
- `document_retrieval/test.py` was renamed to `graph_init.py` so it no longer
  shadows Python’s standard `test` package.
- Vendored NLTK corpora and editor backup files (`*~`) were removed.
- Google Custom Search credentials are read from environment variables.

## License

See [LICENSE](LICENSE).

# Concept Graphs

Algorithms and tools for building **concept graphs** from educational video
transcripts and documents: keyphrase extraction, taxonomy / semantic-network
construction, document retrieval over those graphs, and a Processing-based
explorer UI.

> **Runtime note.** This repository targets **Python 3.10+** with type-annotated
> modules.

## Repository layout

```
concept-graphs/
├── keyphrase_extraction/     # Feature pipeline + classifier (canonical package)
├── document_retrieval/       # Concept-graph build, analysis, retrieval, web UI
├── google_pdf_search/        # Google Custom Search → PDF → text helpers
├── visualization/
│   └── concept_explorer/     # Processing (Java mode) concept browser
├── fast_keyphrase_extraction/# Thin pointer; use keyphrase_extraction/batch.py
├── docs/                     # PDF / ODT project documentation
├── requirements.txt
└── LICENSE
```

| Module | Purpose |
|--------|---------|
| [`keyphrase_extraction/`](keyphrase_extraction/) | Preprocess → features → table → Naive Bayes |
| [`document_retrieval/`](document_retrieval/) | Graph core, retrieval, analysis, taxonomy, web demos |
| [`google_pdf_search/`](google_pdf_search/) | Search, download, and convert PDFs |
| [`visualization/concept_explorer/`](visualization/concept_explorer/) | Processing sketch for browsing subgraphs |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

Keyphrase classification uses scikit-learn (`classifiers.naive_bayes`).

## How to run

Always run commands from the **module root** so relative `data/` paths resolve.

```bash
# Keyphrase features
cd keyphrase_extraction
python -m pipeline ds1.txt --stemmer none --max-gram 3
python batch.py --stemmer none --max-gram 3

# Document retrieval / graph build
cd ../document_retrieval
python -m core.graph_init
python -m retrieval.bag_of_words "stack queue tree"

# Google PDF search
cd ../google_pdf_search
export GOOGLE_API_KEY=...
export GOOGLE_CSE_ID=...
python search_download.py
```

Open `visualization/concept_explorer/` in the [Processing](https://processing.org/)
IDE (Java mode). Media and JSON live under that sketch’s `data/` folder.

See each module’s `README.md` for details.

## License

See [LICENSE](LICENSE).

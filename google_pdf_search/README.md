# Google PDF search helpers

Utilities that query [Google Custom Search](https://developers.google.com/custom-search)
for PDFs related to a keyphrase list, download them, and prepare text for the
keyphrase pipeline.

## Credentials

Do **not** commit API keys. Export them before running:

```bash
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CSE_ID="your-custom-search-engine-id"
python gcs.py
```

## Layout

```
google_pdf_search/
├── gcs.py              # Custom Search + PDF download
├── dir.py              # PDF → text via pdfminer
├── txt2ascii.py        # unicode normalization
├── txt2keyphrase.py    # hand off text files to keyphrase scripts
└── data/               # key lists, counters, progress markers
```

Optional path argument (defaults to `data/`):

```bash
python txt2ascii.py /path/to/transcripts
python txt2keyphrase.py /path/to/transcripts
```

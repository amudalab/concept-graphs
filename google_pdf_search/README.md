# Google PDF search helpers

Query Google Custom Search for PDFs, download them, and convert to text.

Requires **Python 3.10+**.

## Credentials

```bash
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CSE_ID="your-custom-search-engine-id"
python search_download.py
```

## Commands

```bash
python search_download.py          # Custom Search + PDF download
python pdf_to_text.py Gsearch/     # PDF → text via pdfminer.six
python normalize_ascii.py data/    # normalize transcripts
python run_keyphrase.py data/      # hand off to keyphrase pipeline
```

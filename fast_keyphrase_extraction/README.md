# Fast keyphrase extraction

A compact batch runner for the same audio keyphrase features as
`keyphrase_extraction/`. Useful when you want to process a folder of
transcripts with one entry point.

Run from this directory.

## Layout

```
fast_keyphrase_extraction/
├── automate.py / automate_tfidf.py   # batch drivers
├── keyextract.py / txt2ascii.py
├── audio_features/ / preprocess_audio/
└── data/
    ├── transcripts/   # inputs
    └── output/        # generated features
```

## Usage

```bash
# Ensure data/txt2keyphrase.txt exists (skip list of already-processed files)
python automate.py
python automate_tfidf.py
```

Default input folder is `data/transcripts/`.

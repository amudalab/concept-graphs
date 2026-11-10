# Keyphrase extraction

Feature-based keyphrase extraction for lecture audio transcripts and
slide/video text, plus a scikit-learn Naive Bayes classifier.

Requires **Python 3.10+**. Run every command from this directory.

## Layout

```
keyphrase_extraction/
├── features/        # cscore, cue, tfidf, local_span, dispersion, feature_table
├── preprocess/      # POS tagging, n-grams, video stem/ngrams
├── video/           # slide occurrence features
├── classifiers/     # Naive Bayes + training-table merge
├── lexicons/        # stopwords + cue phrases
├── _internal/       # paths, stemming, IO, text helpers
├── pipeline.py      # end-to-end single-lecture runner
├── batch.py         # batch runner (ex fast_keyphrase_extraction)
├── cli.py           # unified subcommands
├── config/          # POS filters, word lists on disk
├── scripts/         # shell drivers
└── data/            # transcripts, keys, generated features
```

## Quick start

```bash
python -m pipeline ds1.txt --stemmer none --max-gram 3
python batch.py --stemmer none --max-gram 3

python -m features.cscore ds1.txt none
python -m features.feature_table ds1.txt \
  'cscore,localspan,cuewords,dispersion,tfidf' \
  '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none

python -m classifiers.naive_bayes TrainingDataSet1.tab ds1.txt
```

# Keyphrase extraction

Feature-based keyphrase extraction for lecture audio transcripts and
slide/video text, plus Naive Bayes experiments (ICMR-style studies).

Run every command from this directory (`keyphrase_extraction/`).

## Layout

```
keyphrase_extraction/
├── audio_features/       # cscore, cue, dispersion, localspan, tfidf, …
├── video_features/       # contiguous / frequency occurrence ratios, max height
├── preprocess_audio/     # POS tagging, n-gram generation
├── preprocess_video/     # slide text stemming & gram extraction
├── common/               # shared writers, stemmers, stopword lists, pipeline sh
├── ml/
│   ├── naive_bayes/      # Orange-based classifiers
│   ├── test_data/        # feature-table writer for test transcripts
│   └── training_data/    # training-set assembly (write_all.py)
├── config/               # POS filter word lists
├── scripts/              # day-to-day pipeline shell scripts
│   └── experiments/      # longer ICMR / ablation study scripts
├── tools/                # small utilities (keyextract3.py)
└── data/
    ├── transcripts/              # input lecture transcripts
    ├── corrected_transcripts/    # human-corrected variants
    ├── keys/                     # gold keyphrase lists (.key)
    ├── output/                   # generated feature files (.tab, _tfidf.txt, …)
    ├── video_text_slides/        # per-lecture slide text dumps
    ├── training_data/            # assembled TrainingDataSet*.tab
    └── legacy_transcripts/       # older transcript snapshots
```

## Typical pipeline

```bash
# POS → grams → features → combined table
sh scripts/pos1.sh ds5.txt none enable
sh scripts/grams.sh ds5.txt 3 config/pos_filter.txt none
sh scripts/cscore.sh ds5.txt none
sh scripts/tfidf.sh none 3 ds5.txt
sh scripts/localspan.sh ds5.txt none 3
sh scripts/cue.sh ds5.txt none 3
sh scripts/dispersion.sh ds5.txt
python ml/test_data/write.py ds5.txt \
  'cscore,localspan,cuewords,dispersion,tfidf' \
  '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none
```

Or run the bundled demo: `sh scripts/keyphraseExt.sh`.

The fuller audio+video driver lives at `common/keyphrase.sh` (it `cd`s to this
module root automatically).

## Data paths inside Python

Feature scripts read/write under `data/output` and `data/transcripts` relative
to this module root. Do not invoke them from another working directory unless
you adjust those folder variables.

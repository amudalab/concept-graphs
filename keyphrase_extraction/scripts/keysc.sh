#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
sh scripts/pos1.sh $1 none enable
sh scripts/grams.sh $1 3 config/pos_filter.txt none
sh scripts/cue.sh $1 none 3
sh scripts/localspan.sh $1 none 3
sh scripts/tfidf.sh none 3 $1
sh scripts/cscore.sh $1 none
sh scripts/dispersion.sh $1
python -m features.feature_table $1 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none



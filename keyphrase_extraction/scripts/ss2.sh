#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
sh scripts/pos1.sh $1 none enable
sh scripts/grams.sh $1 3 config/pos_filter.txt none
sh scripts/tfidf.sh none 3 $1
sh scripts/localspan.sh $1 none 3
sh scripts/cue.sh $1 none 3
sh scripts/cscore.sh $1 none
sh scripts/dispersion.sh $1
python ml/test_data/write.py $1 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


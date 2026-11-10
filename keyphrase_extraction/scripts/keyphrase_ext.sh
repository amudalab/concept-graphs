#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
python -m preprocess.pos_tag 0000172.txt none enable
python -m preprocess.ngrams 0000172.txt 3 none
python -m features.cscore 0000172.txt none
python -m features.tfidf "none" 3 "0000172.txt"
python -m features.local_span 0000172.txt 3 "none"
python -m features.cue 0000172.txt "none" 3
python -m features.dispersion 0000172.txt 3 "none"
python -m features.feature_table 0000172.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none

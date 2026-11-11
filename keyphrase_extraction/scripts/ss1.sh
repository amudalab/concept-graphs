#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
sh scripts/pos1.sh ds1.txt none enable
sh scripts/grams.sh ds1.txt 3 config/pos_filter.txt none
sh scripts/tfidf.sh none 3 ds1.txt
sh scripts/localspan.sh ds1.txt none 3
sh scripts/cue.sh ds1.txt none 3
sh scripts/cscore.sh ds1.txt none
sh scripts/dispersion.sh ds1.txt
python -m features.feature_table ds1.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


sh scripts/pos1.sh ds2.txt none enable
sh scripts/grams.sh ds2.txt 3 config/pos_filter.txt none
sh scripts/tfidf.sh none 3 ds2.txt
sh scripts/localspan.sh ds2.txt none 3
sh scripts/cue.sh ds2.txt none 3
sh scripts/cscore.sh ds2.txt none
sh scripts/dispersion.sh ds2.txt
python -m features.feature_table ds2.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


sh scripts/pos1.sh ds3.txt none enable
sh scripts/grams.sh ds3.txt 3 config/pos_filter.txt none
sh scripts/tfidf.sh none 3 ds3.txt
sh scripts/localspan.sh ds3.txt none 3
sh scripts/cue.sh ds3.txt none 3
sh scripts/cscore.sh ds3.txt none
sh scripts/dispersion.sh ds3.txt
python -m features.feature_table ds3.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


sh scripts/pos1.sh ds4.txt none enable
sh scripts/grams.sh ds4.txt 3 config/pos_filter.txt none
sh scripts/tfidf.sh none 3 ds4.txt
sh scripts/localspan.sh ds4.txt none 3
sh scripts/cue.sh ds4.txt none 3
sh scripts/cscore.sh ds4.txt none
sh scripts/dispersion.sh ds4.txt
python -m features.feature_table ds4.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none

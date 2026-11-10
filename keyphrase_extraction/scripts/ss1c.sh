#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
sh scripts/pos1.sh ds5.txt none enable
sh scripts/grams.sh ds5.txt 3 config/pos_filter.txt none
sh scripts/tfidf.sh none 3 ds5.txt
sh scripts/localspan.sh ds5.txt none 3
sh scripts/cue.sh ds5.txt none 3
sh scripts/cscore.sh ds5.txt none
sh scripts/dispersion.sh ds5.txt
python ml/test_data/write.py ds5.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


sh scripts/pos1.sh ds6.txt none enable
sh scripts/grams.sh ds6.txt 3 config/pos_filter.txt none
sh scripts/tfidf.sh none 3 ds6.txt
sh scripts/localspan.sh ds6.txt none 3
sh scripts/cue.sh ds6.txt none 3
sh scripts/cscore.sh ds6.txt none
sh scripts/dispersion.sh ds6.txt
python ml/test_data/write.py ds6.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


sh scripts/pos1.sh ds7.txt none enable
sh scripts/grams.sh ds7.txt 3 config/pos_filter.txt none
sh scripts/tfidf.sh none 3 ds7.txt
sh scripts/localspan.sh ds7.txt none 3
sh scripts/cue.sh ds7.txt none 3
sh scripts/cscore.sh ds7.txt none
sh scripts/dispersion.sh ds7.txt
python ml/test_data/write.py ds7.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


sh scripts/pos1.sh ds8.txt none enable
sh scripts/grams.sh ds8.txt 3 config/pos_filter.txt none
sh scripts/tfidf.sh none 3 ds8.txt
sh scripts/localspan.sh ds8.txt none 3
sh scripts/cue.sh ds8.txt none 3
sh scripts/cscore.sh ds8.txt none
sh scripts/dispersion.sh ds8.txt
python ml/test_data/write.py ds8.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none

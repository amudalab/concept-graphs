sh pos1.sh ds5.txt none enable
sh grams.sh ds5.txt 3 pos_filter.txt none
sh tfidf.sh none 3 ds5.txt
sh localspan.sh ds5.txt none 3
sh cue.sh ds5.txt none 3
sh cscore.sh ds5.txt none
sh dispersion.sh ds5.txt
python ml_audio/testData/write.py ds5.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


sh pos1.sh ds6.txt none enable
sh grams.sh ds6.txt 3 pos_filter.txt none
sh tfidf.sh none 3 ds6.txt
sh localspan.sh ds6.txt none 3
sh cue.sh ds6.txt none 3
sh cscore.sh ds6.txt none
sh dispersion.sh ds6.txt
python ml_audio/testData/write.py ds6.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


sh pos1.sh ds7.txt none enable
sh grams.sh ds7.txt 3 pos_filter.txt none
sh tfidf.sh none 3 ds7.txt
sh localspan.sh ds7.txt none 3
sh cue.sh ds7.txt none 3
sh cscore.sh ds7.txt none
sh dispersion.sh ds7.txt
python ml_audio/testData/write.py ds7.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


sh pos1.sh ds8.txt none enable
sh grams.sh ds8.txt 3 pos_filter.txt none
sh tfidf.sh none 3 ds8.txt
sh localspan.sh ds8.txt none 3
sh cue.sh ds8.txt none 3
sh cscore.sh ds8.txt none
sh dispersion.sh ds8.txt
python ml_audio/testData/write.py ds8.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none

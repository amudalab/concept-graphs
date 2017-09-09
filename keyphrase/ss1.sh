sh pos1.sh ds1.txt none enable
sh grams.sh ds1.txt 3 pos_filter.txt none
sh tfidf.sh none 3 ds1.txt
sh localspan.sh ds1.txt none 3
sh cue.sh ds1.txt none 3
sh cscore.sh ds1.txt none
sh dispersion.sh ds1.txt
python ml_audio/testData/write.py ds1.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


sh pos1.sh ds2.txt none enable
sh grams.sh ds2.txt 3 pos_filter.txt none
sh tfidf.sh none 3 ds2.txt
sh localspan.sh ds2.txt none 3
sh cue.sh ds2.txt none 3
sh cscore.sh ds2.txt none
sh dispersion.sh ds2.txt
python ml_audio/testData/write.py ds2.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


sh pos1.sh ds3.txt none enable
sh grams.sh ds3.txt 3 pos_filter.txt none
sh tfidf.sh none 3 ds3.txt
sh localspan.sh ds3.txt none 3
sh cue.sh ds3.txt none 3
sh cscore.sh ds3.txt none
sh dispersion.sh ds3.txt
python ml_audio/testData/write.py ds3.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none


sh pos1.sh ds4.txt none enable
sh grams.sh ds4.txt 3 pos_filter.txt none
sh tfidf.sh none 3 ds4.txt
sh localspan.sh ds4.txt none 3
sh cue.sh ds4.txt none 3
sh cscore.sh ds4.txt none
sh dispersion.sh ds4.txt
python ml_audio/testData/write.py ds4.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none

sh pos1.sh $1 none enable
sh grams.sh $1 3 pos_filter.txt none
sh cue.sh $1 none 3
sh localspan.sh $1 none 3
sh tfidf.sh none 3 $1
sh cscore.sh $1 none
sh dispersion.sh $1
python ml_audio/testData/write.py $1 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none



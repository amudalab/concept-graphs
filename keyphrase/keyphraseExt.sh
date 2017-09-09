python preprocess_audio/pos1.py 0000172.txt none enable
python preprocess_audio/grams.py 0000172.txt 3 none
python audio_features/cscore.py 0000172.txt none
python audio_features/tfidf.py "none" 3 "0000172.txt"
python audio_features/localspan.py 0000172.txt 3 "none"
python audio_features/cue.py 0000172.txt "none" 3
python audio_features/dispersiontest.py 0000172.txt 3 "none"
python keyphrase/write.py 0000172.txt 'cscore,localspan,cuewords,dispersion,tfidf' '_cscore.txt,_localspan.txt,_cue.txt,_disp.txt,_tfidf.txt' none

transcript_list=$1

for transcript in $transcript_list; do 
	python audio_features/dispersiontest.py $transcript
done


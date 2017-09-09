transcript_list=$1
stemmer=$2
pos_tagging=$3

for transcript in $transcript_list; do 
	python preprocess_audio/pos1.py $transcript $stemmer $pos_tagging
done

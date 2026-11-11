#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
transcript_list=$1
gramSize=$2
posFilter_file=$3
stemmer=$4
echo $transcript_list
echo "Hello"
#for transcript in $transcript_list; do
	echo "Hi"
	echo  $posFilter_file
	echo "printed"
	if [ "$posFilter_file" = "none" ]
	then
		echo $transcript_list
		echo "first if"		
		python -m preprocess.ngrams $transcript_list $gramSize $stemmer
		
	elif [ "$posFilter_file" = "default_posfilter" ]
	then
		echo "second if"
		python -m preprocess.ngrams $transcript_list $gramSize config/pos_filter.txt $stemmer
	else
		echo "third else"
		python -m preprocess.ngrams $transcript_list $gramSize $posFilter_file $stemmer
	fi
#done


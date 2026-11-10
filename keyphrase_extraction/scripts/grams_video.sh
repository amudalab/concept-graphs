#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
transcript_list=$1
gramSize=$2

for transcript in $transcript_list; do 
	python -m preprocess.video_ngrams $transcript $gramSize
done




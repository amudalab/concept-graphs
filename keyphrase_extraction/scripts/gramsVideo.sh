#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
transcript_list=$1
gramSize=$2

for transcript in $transcript_list; do 
	python preprocess_video/extractgrams.py $transcript $gramSize
done




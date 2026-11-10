#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
transcript_list=$1
stemmer=$2
gramSize=$3

for transcript in $transcript_list; do 
	python -m features.cue  $transcript $stemmer $gramSize
done





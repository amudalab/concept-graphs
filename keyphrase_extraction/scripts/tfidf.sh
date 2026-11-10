#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
stemmer=$1
gramSize=$2
transcript_list=$3

for transcript in $transcript_list; do 
	python -m features.tfidf $stemmer $gramSize $transcript
done

#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
transcript_list=$1
gramSize=$2
stemmer=$3

for transcript in $transcript_list; do 
	python -m features.local_span $transcript $gramSize $stemmer
done





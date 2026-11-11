#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
transcript_list=$1
stemmer=$2
pos_tagging=$3

for transcript in $transcript_list; do 
	python -m preprocess.pos_tag $transcript $stemmer $pos_tagging
done

#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
transcript_list=$1
stemmer=$2

for transcript in $transcript_list; do 
	python audio_features/cscore.py $transcript $stemmer
done

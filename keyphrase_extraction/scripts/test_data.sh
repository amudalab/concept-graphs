#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
transcript_list=$1
feature_list=$2
feature_ext=$3
stemmer=$4

for transcript in $transcript_list; do 
	python -m features.feature_table $transcript $feature_list $feature_ext $stemmer
done

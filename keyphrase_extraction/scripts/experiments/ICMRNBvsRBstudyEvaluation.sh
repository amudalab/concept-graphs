#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
transcript_list=$1

echo "evaluation"

for transcript in $transcript_list; do 
	echo $transcript
	python ICMRNBvsRBstudyevaluation.py $transcript Porter-Stemmer
	echo "done"
done

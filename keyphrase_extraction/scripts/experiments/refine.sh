#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
transcript_list=$1

echo "refine"

for transcript in $transcript_list; do 
	echo $transcript
	python refine.py $transcript
	echo "done"
done

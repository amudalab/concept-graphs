#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
transcript_list=$1

echo "After applying rules"

for transcript in $transcript_list; do 
	echo $transcript
	python ruleBased.py $transcript
	echo "done"
done

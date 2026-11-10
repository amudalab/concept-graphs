#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
transcript_list=$1

echo "Gramwise Seperation"

for transcript in $transcript_list; do 
	echo $transcript
	python gramwiseTrainingandTesting.py $transcript
	echo "done"
done





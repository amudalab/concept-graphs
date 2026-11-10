#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
testing_list=$1
trainingData=$2

echo "Keyphrase extraction"

for testing in $testing_list; do 
	echo $testing
	python ml/naive_bayes/NaiveBayes_final.py $trainingData $testing
	echo "done"
done

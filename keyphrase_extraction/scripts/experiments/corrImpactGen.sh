#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
testing_list=$1

echo "Corr Impact"

for testing in $testing_list; do 
	echo $testing
	python ml/naive_bayes/corrImpact.py $testing
	echo "done"
done

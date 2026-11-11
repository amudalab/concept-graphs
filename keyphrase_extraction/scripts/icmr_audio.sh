#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
#<testing> : accepts <transcript_name>.txt as input from user
#<trainingData> :  accepts <trainingData>.tab as input from user 

testing=$1
trainingData=$2


python -m classifiers.naive_bayes $trainingData $testing



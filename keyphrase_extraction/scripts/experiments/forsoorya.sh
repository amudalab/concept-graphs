#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
trainingDataInputList=$1
trainingDataSetName=$2
testing_list=$3

echo "training data file Generation"
echo $trainingDataInputList
echo $trainingDataSetName

python -m classifiers.write_all $trainingDataInputList $trainingDataSetName data/output data/keys data/training_data Porter-Stemmer

cp TrainingDataSet/$trainingDataSetName data/training_data

for testing in $testing_list; do 
	echo $testing
	python ml/naive_bayes/Naive-Bayes_Myversion.py $trainingDataSetName $testing
	python evaluation.py $testing Porter-Stemmer
	echo "done"
done


echo "done"


#./forsoorya.sh 'ds1.tab,ds3,ds5,ds7,ds11,ds13,ml2,ml4,ml6,ml8,ml10,ml12,iit-d-ca-CA-LEC-1,iit-d-ca-CA-LEC3,iit-d-ca-CA-LEC-5,iit-d-ca-CA-LEC-7,iit-d-ca-CA-LEC9,cg2,cg4,ppl1,pp3,ppl5,dbms-DBMS-lecture-2,embsys,bio1,it1' TrainingDataSet1.tab 'ds10.txt ds11.txt'

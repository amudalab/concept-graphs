#!/bin/sh
cd "$(dirname "$0")/../.." || exit 1
echo "training data file Generation"

python -m classifiers.write_all cg4.tab,cg5.tab,ds3.tab,ds4.tab,ds5.tab,ds6.tab,ds7.tab,ds8.tab,ppl3.tab,ppl4.tab,ppl5.tab TrainingDataSet1.tab data/output data/keys data/training_data Porter-Stemmer

python -m classifiers.write_all cg5.tab,ds7.tab,ds8.tab,ds10.tab,ds11.tab,ds12.tab,ds13.tab,ppl2.tab,ppl3.tab,ppl4.tab,ppl5.tab,ml8.tab,ml9.tab,ml10.tab,ml11.tab,ml12.tab TrainingDataSet2.tab data/output data/keys data/training_data Porter-Stemmer

python -m classifiers.write_all ppl2.tab,ppl3.tab,ppl4.tab,ppl5.tab,ml2.tab,ml3.tab,ml4.tab,ml5.tab,ml6.tab,ml7.tab,ml8.tab,ml9.tab,ml10.tab,ml11.tab,ml12.tab,embsys.tab TrainingDataSet3.tab data/output data/keys data/training_data Porter-Stemmer

python -m classifiers.write_all comparch1.tab,dbms1.tab,it1.tab,embsys.tab,wolfram.tab,ppl1.tab,ppl2.tab,ds3.tab,ds4.tab,ml1.tab,ml2.tab,ml3.tab,ml4.tab,ml5.tab,ds5.tab,ml6.tab TrainingDataSet4.tab data/output data/keys data/training_data Porter-Stemmer

python -m classifiers.write_all cg4.tab,cg5.tab,comparch1.tab,dbms1.tab,ds10.tab,ds11.tab,ds12.tab,ds13.tab,ds3.tab,ds4.tab,ds5.tab,ds6.tab,ds7.tab,ds8.tab,embsys.tab,it1.tab,ml1.tab,ml10.tab,ml11.tab,ml12.tab,ml2.tab,ml3.tab,ml4.tab,ml5.tab,ml6.tab,ml7.tab,ml8.tab,ml9.tab,ppl1.tab,ppl2.tab,ppl3.tab,ppl4.tab,ppl5.tab,wolfram.tab TrainingDataSet5.tab data/output data/keys data/training_data Porter-Stemmer

echo "done"

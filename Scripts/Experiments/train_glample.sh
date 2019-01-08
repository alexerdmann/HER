model_loc=$1
train=$PWD/$2
dev=$PWD/$3
test=$PWD/$4
preTrained=$PWD/$5
n_epochs=$6
current=$PWD

cd ../tagger
# source deactivate
# source activate py27

./train.py --train $train --dev $dev --test $test --model_loc $model_loc --pre_emb $preTrained --n_epochs $n_epochs

# source deactivate
# source activate py36
cd $current







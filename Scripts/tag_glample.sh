model_loc=$1
test_in=$PWD/$2
test_out=$PWD/$3

cd ../tagger
# source deactivate
# source activate py27

./tagger.py --model models/$model_loc --input $test_in --output $test_out --model_loc $model_loc

# source deactivate
# source activate py36
cd $current